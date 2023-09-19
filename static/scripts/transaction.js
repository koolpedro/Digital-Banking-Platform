// transaction.js

document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit");
    const transactionStatus = document.getElementById("transaction-status");

    submitButton.addEventListener("click", function () {
        // Get selected bank, source account, destination account, amount, and description
        const selectedBank = document.querySelector('input[name="bank"]:checked');
        const sourceAccount = document.getElementById("source-account").value;
        const destinationAccount = document.getElementById("destination-account").value;
        const amount = document.getElementById("amount").value;
        const description = document.getElementById("description").value;

        // Perform the transaction (you'll implement this part)
        // For demonstration purposes, just display a message
        const transactionResult = `Transaction Details:
            Bank: ${selectedBank ? selectedBank.value : 'N/A'}
            Source Account: ${sourceAccount}
            Destination Account: ${destinationAccount}
            Amount: ${amount}
            Description: ${description}`;

        // Display the transaction status
        transactionStatus.textContent = transactionResult;
    });
});

