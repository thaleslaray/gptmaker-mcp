"""GPTMaker tools — Agent Diagnostics."""

import asyncio
import json
from datetime import datetime
from typing import Any

import httpx

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()

BEHAVIOR_CHAR_LIMIT = 3000
CONTEXT_INTERACTION_LIMIT = 20

# Models with higher hallucination risk (weaker instruction following)
WEAK_MODELS = {"GPT_4_O_MINI", "GPT_4_1_MINI", "CLAUDE_3_5_HAIKU", "DEEPINFRA_LLAMA3_3"}


async def audit_agent(agent_id: str) -> str:
    """Run a complete diagnostic audit of an agent's configuration.

    Checks agent info, settings, behavior, trainings, intentions, transfer rules,
    idle actions, channels, webhooks, and credits. Returns a structured report
    with warnings, errors, and recommendations.

    Args:
        agent_id: Agent ID to audit.
    """
    now = datetime.now()

    # Fetch everything in parallel
    results = await asyncio.gather(
        _client.get(f"/v2/agent/{agent_id}"),
        _client.get(f"/v2/agent/{agent_id}/settings"),
        _client.get(f"/v2/agent/{agent_id}/webhooks"),
        _client.get(f"/v2/agent/{agent_id}/intentions", params={"page": 1, "pageSize": 50}),
        _client.get(f"/v2/agent/{agent_id}/transfer-rules"),
        _client.get(f"/v2/agent/{agent_id}/idle-actions"),
        _client.get(f"/v2/agent/{agent_id}/search", params={"page": 1, "pageSize": 50}),
        _client.get(
            f"/v2/agent/{agent_id}/credits-spent",
            params={"year": now.year, "month": now.month},
        ),
        _client.get(f"/v2/agent/{agent_id}/list-behavior-history", params={"page": 1, "pageSize": 5}),
        return_exceptions=True,
    )

    agent, settings, webhooks, intentions_resp, transfer_rules, idle_actions, channels_resp, credits, behavior_history = results

    report: dict[str, Any] = {
        "agent_id": agent_id,
        "audited_at": now.isoformat(),
        "score": 100,
        "errors": [],
        "warnings": [],
        "ok": [],
        "recommendations": [],
        "sections": {},
    }

    def error(msg: str) -> None:
        report["errors"].append(msg)
        report["score"] -= 15

    def warning(msg: str) -> None:
        report["warnings"].append(msg)
        report["score"] -= 5

    def ok(msg: str) -> None:
        report["ok"].append(msg)

    def rec(msg: str) -> None:
        report["recommendations"].append(msg)

    # ── AGENT INFO ──────────────────────────────────────────────────────────
    if isinstance(agent, Exception):
        error(f"Não foi possível carregar o agente: {agent}")
    else:
        name = agent.get("name", "sem nome")
        active = agent.get("active", False)
        behavior = agent.get("behavior") or ""
        behavior_len = len(behavior)

        report["sections"]["agent"] = {
            "name": name,
            "active": active,
            "behavior_chars": behavior_len,
            "behavior_limit": BEHAVIOR_CHAR_LIMIT,
        }

        if not active:
            warning(f"Agente '{name}' está INATIVO — não responde mensagens")
        else:
            ok(f"Agente '{name}' está ativo")

        if not behavior.strip():
            error("Campo 'Comportamento' está vazio — agente sem personalidade ou escopo definido")
        elif behavior_len > BEHAVIOR_CHAR_LIMIT:
            error(f"Comportamento excede o limite ({behavior_len}/{BEHAVIOR_CHAR_LIMIT} chars) — será truncado pela plataforma")
        elif behavior_len > int(BEHAVIOR_CHAR_LIMIT * 0.85):
            warning(f"Comportamento quase no limite ({behavior_len}/{BEHAVIOR_CHAR_LIMIT} chars) — pouco espaço para ajustes")
        else:
            ok(f"Comportamento dentro do limite ({behavior_len}/{BEHAVIOR_CHAR_LIMIT} chars)")

    # ── SETTINGS ────────────────────────────────────────────────────────────
    if isinstance(settings, Exception):
        warning(f"Não foi possível carregar as configurações: {settings}")
    else:
        model = settings.get("prefferModel") or settings.get("preferModel") or "não definido"
        knowledge_by_function = settings.get("knowledgeByFunction", False)
        on_lack_knowledge = settings.get("onLackKnowLedge") or settings.get("onLackKnowledge") or ""
        limit_subjects = settings.get("limitSubjects", False)
        enabled_human_transfer = settings.get("enabledHumanTransfer", False)
        timezone = settings.get("timezone") or ""
        max_daily = settings.get("maxDailyMessages")
        split_messages = settings.get("splitMessages", False)

        report["sections"]["settings"] = {
            "model": model,
            "knowledge_by_function": knowledge_by_function,
            "on_lack_knowledge": on_lack_knowledge,
            "limit_subjects": limit_subjects,
            "enabled_human_transfer": enabled_human_transfer,
            "timezone": timezone,
            "max_daily_messages": max_daily,
            "split_messages": split_messages,
        }

        ok(f"Modelo configurado: {model}")

        if model in WEAK_MODELS:
            warning(f"Modelo '{model}' tem maior tendência a alucinações em instruções complexas — considere GPT_4_O, GPT_4_1 ou CLAUDE_3_7_SONNET para casos críticos")

        if not knowledge_by_function:
            warning("knowledgeByFunction está DESATIVADO — agente pode responder sem consultar os treinamentos primeiro (causa comum de alucinações)")
            rec("Ative knowledgeByFunction=true via update_agent_settings para forçar consulta à base de conhecimento")
        else:
            ok("knowledgeByFunction ativado — agente consulta treinamentos antes de responder")

        if not on_lack_knowledge:
            warning("onLackKnowledge não configurado — agente pode inventar informações quando não souber a resposta")
            rec("Configure onLackKnowledge com uma mensagem padrão ex: 'Não tenho essa informação no momento. Posso ajudar com outra coisa?'")
        else:
            ok(f"onLackKnowledge configurado: '{on_lack_knowledge[:60]}...' " if len(on_lack_knowledge) > 60 else f"onLackKnowledge configurado: '{on_lack_knowledge}'")

        if not limit_subjects:
            warning("limitSubjects está DESATIVADO — agente pode responder qualquer assunto fora do escopo")
        else:
            ok("limitSubjects ativado — agente restrito ao escopo configurado")

        if not timezone:
            warning("Timezone não definido — agendamentos e follow-ups podem ter horário incorreto")
            rec("Configure timezone=America/Sao_Paulo (ou o fuso do cliente) via update_agent_settings")
        else:
            ok(f"Timezone: {timezone}")

        if not max_daily:
            rec("Considere definir max_daily_messages para controlar custo e evitar loops infinitos com outros bots")

        if not enabled_human_transfer:
            warning("Transferência para humano está DESATIVADA — agente não pode escalar atendimentos")
        else:
            ok("Transferência para humano ativada")

    # ── WEBHOOKS ─────────────────────────────────────────────────────────────
    if isinstance(webhooks, Exception):
        warning(f"Não foi possível carregar os webhooks: {webhooks}")
    else:
        wh = {
            "onNewMessage": webhooks.get("onNewMessage"),
            "onLackKnowledge": webhooks.get("onLackKnowLedge") or webhooks.get("onLackKnowledge"),
            "onTransfer": webhooks.get("onTransfer"),
            "onFirstInteraction": webhooks.get("onFirstInteraction"),
            "onStartInteraction": webhooks.get("onStartInteraction"),
            "onFinishInteraction": webhooks.get("onFinishInteraction"),
            "onCreateEvent": webhooks.get("onCreateEvent"),
            "onCancelEvent": webhooks.get("onCancelEvent"),
        }
        configured = [k for k, v in wh.items() if v]
        report["sections"]["webhooks"] = wh

        if not configured:
            rec("Nenhum webhook de evento configurado — configure onFinishInteraction ou onTransfer para integrar com Make/n8n/CRM")
        else:
            ok(f"Webhooks configurados: {', '.join(configured)}")

        # Test configured webhooks
        webhook_tests = {}
        for key, url in wh.items():
            if url:
                status = await _test_url(url)
                webhook_tests[key] = {"url": url, "status": status}
                if status in (200, 201, 202, 204):
                    ok(f"Webhook {key} respondendo ({status}): {url}")
                elif status == 0:
                    warning(f"Webhook {key} inacessível (timeout/erro de rede): {url}")
                else:
                    warning(f"Webhook {key} retornou HTTP {status}: {url}")
        if webhook_tests:
            report["sections"]["webhook_tests"] = webhook_tests

    # ── TRAININGS ────────────────────────────────────────────────────────────
    trainings_data = await _safe_get(f"/v2/agent/{agent_id}/trainings", params={"page": 1, "pageSize": 50})
    if trainings_data is None:
        warning("Não foi possível carregar os treinamentos")
    else:
        items = trainings_data.get("items") or trainings_data.get("content") or (trainings_data if isinstance(trainings_data, list) else [])
        total = len(items)
        types = [t.get("type", "UNKNOWN") for t in items]
        report["sections"]["trainings"] = {"total": total, "types": types}

        if total == 0:
            error("Agente sem nenhum treinamento — vai alucidar para qualquer pergunta específica")
        elif total < 3:
            warning(f"Apenas {total} treinamento(s) — base de conhecimento fraca")
            rec("Adicione treinamentos com: FAQ, políticas da empresa, produtos/serviços, exemplos de perguntas e respostas")
        else:
            ok(f"{total} treinamento(s) configurado(s): {', '.join(set(types))}")

    # ── INTENTIONS ──────────────────────────────────────────────────────────
    if isinstance(intentions_resp, Exception):
        warning(f"Não foi possível carregar as intenções: {intentions_resp}")
    else:
        items = intentions_resp.get("items") or intentions_resp.get("content") or (intentions_resp if isinstance(intentions_resp, list) else [])
        total = len(items)
        report["sections"]["intentions"] = {"total": total, "issues": []}

        if total == 0:
            rec("Nenhuma intenção configurada — intenções permitem integrar o agente com sistemas externos (CRM, agendamento, etc.)")
        else:
            ok(f"{total} intenção(ões) configurada(s)")
            for intention in items:
                name = intention.get("description") or intention.get("name") or intention.get("id", "sem nome")
                issues = _check_intention(intention)
                if issues:
                    for issue in issues:
                        error_msg = f"Intenção '{name[:50]}': {issue}"
                        report["sections"]["intentions"]["issues"].append(error_msg)
                        warning(error_msg)
                else:
                    ok(f"Intenção '{name[:50]}' OK")

    # ── TRANSFER RULES ──────────────────────────────────────────────────────
    if isinstance(transfer_rules, Exception):
        warning(f"Não foi possível carregar as regras de transferência: {transfer_rules}")
    else:
        items = transfer_rules.get("items") or transfer_rules.get("content") or (transfer_rules if isinstance(transfer_rules, list) else [])
        total = len(items)
        report["sections"]["transfer_rules"] = {"total": total}

        has_human_transfer = not isinstance(settings, Exception) and settings.get("enabledHumanTransfer", False)
        if has_human_transfer and total == 0:
            warning("Transferência para humano está ativada mas não há regras de transferência configuradas — quando e para quem transferir?")
            rec("Crie uma regra de transferência com create_transfer_rule definindo quando e para qual humano/agente transferir")
        elif total > 0:
            ok(f"{total} regra(s) de transferência configurada(s)")

    # ── IDLE ACTIONS ────────────────────────────────────────────────────────
    if isinstance(idle_actions, Exception):
        warning(f"Não foi possível carregar as ações de inatividade: {idle_actions}")
    else:
        items = idle_actions.get("items") or idle_actions.get("content") or (idle_actions if isinstance(idle_actions, list) else [])
        total = len(items)
        report["sections"]["idle_actions"] = {"total": total}

        if total > 0:
            ok(f"{total} ação(ões) de inatividade configurada(s)")
            # Check if timezone is missing (follow-up at wrong hours)
            has_tz = not isinstance(settings, Exception) and bool(settings.get("timezone"))
            if not has_tz:
                warning("Ações de inatividade configuradas mas timezone não definido — follow-ups podem ser enviados de madrugada")

    # ── CHANNELS ────────────────────────────────────────────────────────────
    if isinstance(channels_resp, Exception):
        warning(f"Não foi possível carregar os canais: {channels_resp}")
    else:
        items = channels_resp.get("items") or channels_resp.get("content") or (channels_resp if isinstance(channels_resp, list) else [])
        total = len(items)
        report["sections"]["channels"] = {
            "total": total,
            "channels": [{"name": c.get("name"), "type": c.get("type"), "id": c.get("id")} for c in items],
        }

        if total == 0:
            error("Nenhum canal conectado — agente não pode receber mensagens de nenhuma plataforma")
        else:
            types = [c.get("type", "?") for c in items]
            ok(f"{total} canal(is) conectado(s): {', '.join(types)}")

    # ── CREDITS ─────────────────────────────────────────────────────────────
    if isinstance(credits, Exception):
        warning(f"Não foi possível carregar os créditos: {credits}")
    else:
        spent = credits.get("total") or credits.get("spent") or credits.get("creditsSpent") or 0
        report["sections"]["credits"] = {"spent_this_month": spent}
        if spent:
            ok(f"Créditos consumidos no mês: {spent}")

    # ── BEHAVIOR HISTORY ────────────────────────────────────────────────────
    if not isinstance(behavior_history, Exception):
        items = behavior_history.get("items") or behavior_history.get("content") or []
        if items:
            report["sections"]["recent_behavior"] = f"{len(items)} interação(ões) recente(s) no histórico"

    # ── SCORE ───────────────────────────────────────────────────────────────
    report["score"] = max(0, report["score"])
    if report["score"] >= 85:
        report["health"] = "✅ SAUDÁVEL"
    elif report["score"] >= 60:
        report["health"] = "⚠️ ATENÇÃO"
    else:
        report["health"] = "❌ CRÍTICO"

    report["summary"] = (
        f"{report['health']} — Score: {report['score']}/100 | "
        f"{len(report['errors'])} erro(s), {len(report['warnings'])} aviso(s), "
        f"{len(report['ok'])} OK, {len(report['recommendations'])} recomendação(ões)"
    )

    return json.dumps(report, indent=2, ensure_ascii=False)


def _check_intention(intention: dict) -> list[str]:
    """Validate a single intention and return a list of issues found."""
    issues = []
    type_ = intention.get("type", "")
    url = intention.get("url") or ""
    fields = intention.get("fields") or []
    description = intention.get("description") or ""
    auto_body = intention.get("autoGenerateBody", False)
    auto_params = intention.get("autoGenerateParams", False)
    headers = intention.get("headers") or []
    http_method = (intention.get("httpMethod") or "").upper()

    if type_ == "WEBHOOK":
        if not url:
            issues.append("URL do webhook não configurada — intenção nunca vai disparar")
        elif not (url.startswith("http://") or url.startswith("https://")):
            issues.append(f"URL inválida: '{url}' — deve começar com http:// ou https://")

        if not fields and not auto_body and not auto_params:
            issues.append("Sem campos definidos e autoGenerate desativado — agente não vai coletar dados antes de disparar")

        if http_method == "POST" and not auto_body and not intention.get("requestBody"):
            issues.append("POST sem requestBody e autoGenerateBody=false — webhook vai receber body vazio")

    if len(description) < 20:
        issues.append(f"Descrição muito curta ('{description}') — LLM pode não entender quando acionar esta intenção")

    return issues


async def _test_url(url: str) -> int:
    """Make a HEAD request to a URL and return the HTTP status code (0 = unreachable)."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.head(url, follow_redirects=True)
            return resp.status_code
    except Exception:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json={"test": True}, follow_redirects=True)
                return resp.status_code
        except Exception:
            return 0


async def _safe_get(path: str, params: dict | None = None) -> dict | None:
    """Call GET and return result or None on error."""
    try:
        return await _client.get(path, params=params)
    except Exception:
        return None
