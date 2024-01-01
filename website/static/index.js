function deleteMeal(mealId) {
    fetch('/delete-meal', {
        method: 'POST',
        body: JSON.stringify({ mealId: mealId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function resetTotals(userId) {
    fetch('/reset-totals', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function resetAverages(userId) {
    fetch('/reset-averages', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}
