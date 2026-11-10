import pandas as pd
from src.config import TICKETS_CSV_PATH


def generate_initial_tickets() -> None:
    """Generates realistic Food Delivery operational support tickets across Customers, Merchants, and Couriers."""
    tickets = [
        {
            "ticket_id": "OPS-5001",
            "timestamp": "2026-11-10T18:10:00",
            "user_role": "Customer",
            "order_id": "ORD-99201",
            "raw_message": "Meu pedido está atrasado há mais de 50 minutos, o entregador está parado no mesmo quarteirão no mapa e o restaurante não atende!",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
        {
            "ticket_id": "OPS-5002",
            "timestamp": "2026-11-10T18:14:00",
            "user_role": "Courier",
            "order_id": "ORD-99201",
            "raw_message": "Pneu da moto furou na Av. Agamenon Magalhães com o pedido ORD-99201 na bag. Preciso que realoquem outro entregador urgente, estou em local seguro.",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
        {
            "ticket_id": "OPS-5003",
            "timestamp": "2026-11-10T18:18:00",
            "user_role": "Merchant",
            "order_id": "ORD-98110",
            "raw_message": "O repasse financeiro da quarta-feira veio com R$ 420,00 a menos do que consta no extrato de vendas do portal do parceiro. Solicito auditoria da taxa.",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
        {
            "ticket_id": "OPS-5004",
            "timestamp": "2026-11-10T18:21:00",
            "user_role": "Customer",
            "order_id": "ORD-99305",
            "raw_message": "O lacre de segurança veio rompido e faltou o refrigerante de 2L e uma batata grande. Quero estorno imediato dos itens faltantes.",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
        {
            "ticket_id": "OPS-5005",
            "timestamp": "2026-11-10T18:25:00",
            "user_role": "Merchant",
            "order_id": "ORD-99400",
            "raw_message": "Nosso gestor de pedidos está travando na tela de confirmação e não toca o alerta sonoro quando entra pedido novo. Já reiniciamos o PC.",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
        {
            "ticket_id": "OPS-5006",
            "timestamp": "2026-11-10T18:29:00",
            "user_role": "Customer",
            "order_id": "ORD-99150",
            "raw_message": "Só passando para elogiar o entregador Carlos! Chovendo muito em Recife e a pizza chegou super quente e intacta. Nota 10!",
            "stakeholder_type": "",
            "intent_category": "",
            "sentiment": "",
            "urgency_sla": "",
            "recommended_action": "",
            "suggested_reply": "",
            "status": "PENDING",
        },
    ]

    df = pd.DataFrame(tickets)
    df.to_csv(TICKETS_CSV_PATH, index=False)
    print(f"✅ Created {len(df)} operational tickets at: {TICKETS_CSV_PATH}")


if __name__ == "__main__":
    generate_initial_tickets()