# Backlog de Tools MCP - GPTMaker
> Gerado de análise de 80.963 linhas de chat de suporte

## Frequência de Temas (linhas 1-60k + período 4)

| Tema | Ocorrências | Impacto |
|------|------------|---------|
| Make/N8N/Zapier | 5.035 | Integração externa |
| Modelos LLM | 4.962 | Seleção/migração de modelo |
| Leads/contatos | 4.526 | Gestão de contatos |
| Canal/conexão | 2.686 | WhatsApp/Instagram desconectado |
| Webhook/integração | 1.652 | Configuração de webhooks |
| Agendamento | 1.467 | Horários, lembretes, follow-up |
| Treinamento | 1.381 | Criar/gerenciar treinamentos |
| Comportamento/prompt | 1.423 | Configurar personalidade do agente |
| Créditos/limite | 1.109 | Consumo e estimativas |
| Atendimento humano | 802 | Transferência para humano |
| Intenções | 771 | Webhooks de saída |
| Agente parado | 438 | Diagnóstico de problemas |
| Campos customizados | 356 | Custom fields |
| Disparos/campanha | 384 | Envio em massa |
| Exportação | 242 | CSV, relatórios |
| Clone/duplicar | 53 | Copiar agente/workspace |

---

## Tier 1 — ALTA PRIORIDADE (Pode ser feito com APIs existentes)

### 1. `bulk_update_agent_model`
**Frequência:** Muito alta (4.962 ocorrências de LLM)
**Problema:** Usuários têm múltiplos agentes usando modelo depreciado (ex: Haiku 3.5, Sonnet 3.7) e precisam migrar todos de uma vez
**O que faz:** Lista todos os agentes usando modelo X e atualiza em lote para modelo Y
**Params:** `from_model`, `to_model`, `workspace_id`, `dry_run`
**APIs:** `list_agents` + `update_agent_settings` ✅

### 2. `find_chat_by_phone`
**Frequência:** Alta (4.526 ocorrências de contatos/número)
**Problema:** Usuários não sabem como achar o `chatId` de um contato pelo número de telefone
**O que faz:** Busca e retorna o chatId a partir do número de telefone
**Params:** `phone`, `workspace_id`
**APIs:** `list_contacts` + `list_chats` ✅

### 3. `monitor_channel_health`
**Frequência:** Alta (2.686 canal/conexão)
**Problema:** Canal do WhatsApp/Instagram desconecta sem aviso; agente para de responder
**O que faz:** Verifica status de todos os canais e retorna quais estão offline/degradados
**Params:** `workspace_id`, `channel_type` (opcional)
**APIs:** `list_channels` + `get_channel` ✅

### 4. `setup_integration_webhook`
**Frequência:** Alta (5.035 Make/N8N + 1.652 webhook)
**Problema:** Configurar intenções com webhooks é complexo; usuários não sabem quais campos enviar
**O que faz:** Cria uma intenção de saída pré-configurada para Make/N8N/Zapier com campos padrão
**Params:** `agent_id`, `platform` (make|n8n|zapier|custom), `webhook_url`, `fields`
**APIs:** `create_intention` ✅

### 5. `setup_human_handoff`
**Frequência:** Alta (802 atendimento humano)
**Problema:** Configurar quando e como transferir para humano é confuso; múltiplos lugares para configurar
**O que faz:** Configura regra de transferência para humano com todas as opções em uma chamada
**Params:** `agent_id`, `trigger_keywords`, `trigger_after_n_messages`, `notify_message`
**APIs:** `create_transfer_rule` + `update_agent_settings` ✅

### 6. `audit_agent` *(já existe no MCP)*
**Frequência:** Alta (438 agente parado + múltiplos diagnósticos)
**Problema:** Agente para de responder sem motivo aparente
**Status:** ✅ Já implementado em `diagnostics.py`

### 7. `bulk_send_messages`
**Frequência:** Alta (384 disparos)
**Problema:** Enviar mensagem para lista de contatos manualmente um a um
**O que faz:** Envia mensagem para lista de contatos com intervalo configurável
**Params:** `agent_id`, `contacts` (lista de phones/chatIds), `message`, `delay_seconds`
**APIs:** `send_message` em loop ✅

### 8. `export_chats_csv`
**Frequência:** Média (242 exportação)
**Problema:** Exportar histórico de conversas para análise/backup
**O que faz:** Exporta conversas de um agente/canal em CSV com todos os campos
**Params:** `agent_id`, `start_date`, `end_date`, `status_filter`
**APIs:** `list_chats` + `get_chat_messages` ✅

### 9. `list_pending_human_support`
**Frequência:** Média (802 atendimento humano)
**Problema:** Não saber quantas/quais conversas estão aguardando atendente humano
**O que faz:** Lista conversas em espera de atendimento humano com tempo de espera
**Params:** `workspace_id`, `agent_id` (opcional)
**APIs:** `list_chats` com filtro de status ✅

### 10. `check_training_coverage`
**Frequência:** Alta (1.381 treinamento)
**Problema:** Não saber se o agente tem treinamento suficiente para responder perguntas do negócio
**O que faz:** Analisa os treinamentos de um agente e identifica gaps de cobertura
**Params:** `agent_id`, `test_questions` (lista de perguntas para verificar)
**APIs:** `list_trainings` + `chat_with_agent` ✅

### 11. `count_agent_characters`
**Frequência:** Alta (1.423 comportamento/prompt)
**Problema:** Usuários excedem limite de caracteres no comportamento do agente sem saber
**O que faz:** Conta caracteres de comportamento, treinamentos e intenções vs. limites
**Params:** `agent_id`
**APIs:** `get_agent` + `list_trainings` + `list_intentions` ✅

### 12. `setup_idle_followup`
**Frequência:** Média (140 inatividade)
**Problema:** Configurar sequência de follow-up de inatividade com múltiplas mensagens é tedioso
**O que faz:** Cria uma sequência de ações de inatividade (ex: 1h → 6h → 24h) de uma vez
**Params:** `agent_id`, `messages` (lista com delay e texto de cada mensagem), `final_action`
**APIs:** `create_idle_action` em sequência ✅

### 13. `tag_contacts_bulk`
**Frequência:** Alta (4.526 leads/contatos)
**Problema:** Segmentar contatos por critério para campanhas/follow-up
**O que faz:** Aplica campo customizado/tag em lote para lista de contatos
**Params:** `workspace_id`, `contact_ids` (ou filtro), `field_name`, `value`
**APIs:** `update_contact` + `list_custom_fields` ✅

### 14. `get_workspace_summary`
**Frequência:** Alta (todos os usuários usam)
**Problema:** Usuários não sabem os IDs de workspaces, agentes, canais; pedem frequentemente
**O que faz:** Retorna resumo do workspace: ID, agentes, canais, créditos, status
**Params:** (nenhum — usa token atual)
**APIs:** `list_workspaces` + `list_agents` + `list_channels` + `get_workspace_credits` ✅

### 15. `test_agent_webhook`
**Frequência:** Alta (1.652 webhook + 771 intenções)
**Problema:** Testar se um webhook de saída está funcionando corretamente
**O que faz:** Dispara um teste de uma intenção/webhook e retorna o resultado
**Params:** `agent_id`, `intention_id`, `test_payload`
**APIs:** `get_intention` + HTTP call de teste ✅

---

## Tier 2 — MÉDIA PRIORIDADE (Precisa de novos endpoints ou pré-processamento)

### 16. `schedule_message`
**Problema:** Agendar mensagem para envio futuro (ex: lembrete de compromisso)
**Precisa:** Endpoint de agendamento com timestamp
**Viabilidade:** Pode ser simulado com cron externo + `send_message`

### 17. `duplicate_agent`
**Problema:** Clonar agente completo para novo cliente
**Precisa:** Duplicar: settings + trainings + intentions + transfer_rules + idle_actions
**Viabilidade:** PARCIAL — pode ser feito com sequência de creates, mas trabalhoso

### 18. `clone_workspace`
**Problema:** Duplicar workspace inteiro como template para novo cliente
**Precisa:** Endpoint nativo de duplicação (sem isso é muito frágil)

### 19. `agent_on_off_schedule`
**Problema:** Ativar/desativar agente em horários específicos
**Precisa:** Cron interno ou scheduler; pode usar `update_agent` para toggle

### 20. `convert_file_to_training`
**Problema:** Usuários não conseguem treinar com XLS/CSV; plataforma só aceita texto/PDF
**Precisa:** Pré-processamento local + `create_training`
**Viabilidade:** PARCIAL — Claude pode processar o arquivo e criar treinamento de texto

---

## Tier 3 — BAIXA PRIORIDADE (Requer novos endpoints da GPTMaker)

| Tool | Precisa |
|------|---------|
| `send_proactive_message` | Endpoint para iniciar conversa ativa com contexto |
| `instagram_dm_filter` | Parâmetro de filtro de tipo de evento no canal |
| `schedule_inactivity_by_hours` | Parâmetro de janela horária na ação de inatividade |
| `conversation_context_injector` | Endpoint de injeção de contexto antes de conversa |
| `analytics_dashboard` | Endpoint de métricas agregadas por agente |
| `user_permission_manager` | API de gestão de usuários/permissões |
| `interaction_limit_per_contact` | Limite por contato (não só por sessão) |

---

## Próximos Passos Recomendados

**Implementar imediatamente (Tier 1, ~2-4h de trabalho):**

1. `bulk_update_agent_model` — resolve migração de modelos depreciados (dor recorrente)
2. `find_chat_by_phone` — elimina a maior causa de confusão de IDs
3. `monitor_channel_health` — detecta proativamente canal offline
4. `setup_integration_webhook` — facilita integração Make/N8N (maior tema do chat)
5. `bulk_send_messages` — habilita disparos em massa
6. `get_workspace_summary` — onboarding mais fácil

Todos podem ser implementados em `src/gptmaker_mcp/tools/composites.py` como ferramentas compostas sobre as primitivas existentes.
