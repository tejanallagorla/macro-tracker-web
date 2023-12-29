function deleteMeal(mealId) {
    fetch('/delete-meal', {
        method: 'POST',
        body: JSON.stringify({ mealId: mealId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}
