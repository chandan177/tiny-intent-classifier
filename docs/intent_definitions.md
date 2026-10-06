# Intent Definitions

## ORDER_STATUS

**Definition:** The customer is asking about the current status, location,
shipping progress, delivery progress, or expected arrival of an existing order.

### Include
- "Where is my order?"
- "Has my package shipped?"
- "When will my order arrive?"
- "Can I track my delivery?"

### Exclude
- Requests to cancel an order → ORDER_CANCEL
- Requests for a refund → REFUND_REQUEST

## ORDER_CANCEL

**Definition:** The customer wants to cancel an existing order before it is completed or delivered.

### Include
- "Cancel my order."
- "I don't want this order anymore."
- "Can you stop my order before it ships?"
- "I placed an order by mistake and want to cancel it."

### Exclude
- Asking where an order is → ORDER_STATUS
- Asking for money back after a completed purchase → REFUND_REQUEST
- Payment could not be completed → PAYMENT_FAILED

## REFUND_REQUEST

**Definition:** The customer is requesting money back for a purchase, charge,
order, or completed transaction.

### Include
- "I want a refund."
- "Can I get my money back?"
- "Please refund my purchase."
- "I returned the product but haven't received my refund."

### Exclude
- Customer wants to stop an active order → ORDER_CANCEL
- Payment cannot be completed → PAYMENT_FAILED
- Customer only asks about delivery → ORDER_STATUS

## PAYMENT_FAILED

**Definition:** The customer is unable to successfully complete a payment
for an order or transaction.

### Include
- "My payment keeps failing."
- "My card is being declined."
- "Why can't I complete the payment?"
- "The payment failed when I tried to place my order."

### Exclude
- Payment succeeded but customer wants the money back → REFUND_REQUEST
- Customer wants to cancel an existing order → ORDER_CANCEL
- Customer cannot access their account → ACCOUNT_ACCESS

## PASSWORD_RESET

**Definition:** The customer wants to reset, recover, or change their password,
including cases where they forgot it.

### Include
- "I forgot my password."
- "How do I reset my password?"
- "I need to change my password."
- "Send me a password reset link."

### Exclude
- Account is locked for a non-password reason → ACCOUNT_ACCESS
- Login problem with no indication that the password is the cause → ACCOUNT_ACCESS
- Payment or order-related problems → their corresponding intent

## ACCOUNT_ACCESS

**Definition:** The customer cannot log in to or access their account for a
reason that is not explicitly a password reset/recovery request.

### Include
- "My account is locked."
- "I can't log in to my account."
- "Why has my account been disabled?"
- "I can't access my profile."

### Exclude
- Explicitly forgot password → PASSWORD_RESET
- Wants to reset/change password → PASSWORD_RESET
- Payment problem → PAYMENT_FAILED
- Order-related problem → corresponding order intent

### Key Boundary

- "I can't log in." → ACCOUNT_ACCESS
- "I can't log in; I forgot my password." → PASSWORD_RESET

