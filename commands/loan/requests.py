LOAN_REQUEST_TIMEOUT = 30

# Pending offers are cleared when the bot restarts.
loan_requests = []


def purge_expired_requests(current_time):
    loan_requests[:] = [
        request for request in loan_requests
        if request["created_at"] + LOAN_REQUEST_TIMEOUT > current_time
    ]


def has_pending_offer(username):
    username = username.lower()
    return any(
        username in (request["lender"].lower(), request["borrower"].lower())
        for request in loan_requests
    )