# Ferramentas Identificadas - Período 4 (linhas 60001-80963)

**Total: 37 ferramentas**

## Clusters principais por frequência de demanda

1. **Gestão de ciclo de atendimento** (itens 1-3, 11, 30, 31): Loop de inatividade pós-objetivo, fechar conversa automaticamente, transferência silenciosa
2. **Disparos e automação proativa** (itens 4, 7, 17, 18, 28, 29): Envio agendado, lembretes, campanhas em lote
3. **Clonagem e reuso** (itens 8, 24): Clonar workspace/agente para múltiplos clientes
4. **Diagnóstico e auditoria** (itens 13, 14, 20, 27, 32): Detectar agente parado, modelo depreciado, comportamento desviando
5. **Localização de IDs** (itens 5, 6): workspaceId e chatId

## Ferramentas (com viabilidade)

### Podem ser feitas com APIs existentes (SIM)

| Tool | O que faz | Prioridade |
|------|-----------|-----------|
| get-workspace-id | Retorna ID do workspace sem consultar docs | ALTA |
| find-chat-by-phone | Busca Chat ID pelo número de telefone | ALTA |
| bulk-update-agent-llm | Atualiza modelo LLM em lote (ex: migrar de Haiku 3.5 depreciado) | ALTA |
| monitor-channel-connection-status | Detecta canais desconectados | ALTA |
| list-chats-by-agent | Lista chats de agente específico com filtros | ALTA |
| export-contacts-csv | Exporta contatos com campos customizados em CSV | ALTA |
| check-agent-health | Diagnóstico completo: status, canal, LLM, treinamentos, teste | ALTA |
| list-chats-pending-human | Lista conversas aguardando atendimento humano | ALTA |
| training-character-counter | Reporta uso de caracteres vs limites por seção | MÉDIA |
| tag-and-segment-contacts | Aplica tags em lote por critério | MÉDIA |
| transfer-agent-silently | Configura transferência sem mensagem ao usuário | MÉDIA |
| detect-inactivity-loop | Detecta conversas em loop de inatividade pós-objetivo | MÉDIA |
| recover-lost-leads | Dispara mensagens para contatos marcados como perdidos | MÉDIA |
| training-status-monitor | Monitora treinamentos travados (stuck em 0%) | MÉDIA |
| webchat-url-generator | Cria canal WebChat e retorna URL formatada | MÉDIA |
| duplicate-agent | Duplica agente completo com todos os configs | MÉDIA |
| multi-agent-routing-setup | Configura roteamento multi-agente em canal único | MÉDIA |
| conversation-audit-by-training | Analisa se agente segue treinamentos configurados | BAIXA |
| generate-agent-prompt | Gera comportamento de agente via LLM + update-agent | BAIXA |
| credit-usage-estimator | Estima créditos baseado em volume e modelo | BAIXA |

### Necessitam de novos endpoints (NÃO/PARCIAL)

| Tool | O que faz | Motivo |
|------|-----------|--------|
| scheduled-message-dispatcher | Agenda envios com régua D-5, D-3, D-0 | Precisa endpoint de agendamento |
| clone-workspace | Duplica workspace inteiro como template | Precisa endpoint nativo de duplicação |
| inactivity-schedule-by-hours | Inatividade com janelas de horário | Parâmetro de horário não existe |
| agent-enable-disable-scheduler | Liga/desliga agente em horários programados | Cron não existe na plataforma |
| send-reminder-before-appointment | Lembretes D-12h, D-6h, D-10min | Precisa agendamento de mensagem futura |
| limit-available-slots-in-response | Limita horários sugeridos na resposta | Hook de pós-processamento não existe |
| proactive-outbound-message | Inicia conversa ativa com contexto injetado | Endpoint específico necessário |
| instagram-dm-filter | Filtra apenas DMs no Instagram | Parâmetro de filtro de evento não existe |
| document-to-training-pipeline | Pipeline para documentos recebidos via chat | Webhook de detecção de mídia |
| webhook-field-mapper | Lista schema/campos disponíveis por webhook | Endpoint de schema não existe |
| interaction-limit-per-contact | Limite de interações por contato (não por sessão) | Funcionalidade não existe |
| conversation-context-injector | Injeta contexto de CRM antes de conversa | Endpoint de injeção de contexto |
| agent-topic-restriction-audit | Testa se restrição de tema funciona | Endpoint de teste de comportamento |
| payment-link-generator | Gera link de pagamento via intenção + webhook | PARCIAL (usa webhook externo) |
| sync-training-from-url | Download de URL + upload como treinamento | PARCIAL (pré-processamento local) |
| convert-training-file | Converte XLS/CSV para formato aceito | PARCIAL (pré-processamento local) |
| bulk-import-contacts | Importa contatos de CSV em lote | PARCIAL (depende de create-contact que pode não existir) |
| bulk-send-message-by-contact-list | Envio em massa com intervalos anti-ban | PARCIAL (send-message individual existe) |
| auto-close-conversation-after-goal | Fecha conversa quando objetivo foi cumprido | Precisa update-chat-status |
