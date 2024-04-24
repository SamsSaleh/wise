function addItem() {
    var totalForms = parseInt(document.getElementById("id_form-TOTAL_FORMS").value);
    var newFormNumber = totalForms;
    document.getElementById("id_form-TOTAL_FORMS").value = newFormNumber + 1 ;

    var lastDiv = document.getElementsByClassName("row")[totalForms - 1];
    var newDiv = document.createElement("div");
    
    newDiv.setAttribute("class", "row");

    newDiv.innerHTML = `
    <div class="col-3">
        <div id="div_id_form-${newFormNumber}-food" class="mb-3">
                <label for="id_form-${newFormNumber}-food" class="form-label requiredField">
                    Food<span class="asteriskField">*</span>
                </label>
                <input type="text" name="form-${newFormNumber}-food" maxlength="100" class="textinput form-control" id="id_form-${newFormNumber}-food">
        </div>
    </div>
    <div class="col-3">
        <div id="div_id_form-${newFormNumber}-fats" class="mb-3">        
            <label for="id_form-${newFormNumber}-fats" class="form-label requiredField">
                Fats<span class="asteriskField">*</span>
            </label>
            <input type="number" name="form-${newFormNumber}-fats" step="any" class="numberinput form-control" id="id_form-${newFormNumber}-fats" onchange="calculateCalories()">
        </div>
    </div>
    <div class="col-3">
        <div id="div_id_form-${newFormNumber}-carbs" class="mb-3">
            <label for="id_form-${newFormNumber}-carbs" class="form-label requiredField">
                Carbs<span class="asteriskField">*</span>
            </label>
            <input type="number" name="form-${newFormNumber}-carbs" step="any" class="numberinput form-control" id="id_form-${newFormNumber}-carbs" onchange="calculateCalories()">
        </div>
    </div>
    <div class="col-3">
        <div id="div_id_form-${newFormNumber}-protein" class="mb-3">
            <label for="id_form-${newFormNumber}-protein" class="form-label requiredField">
                Protein<span class="asteriskField">*</span>
            </label>
            <input type="number" name="form-${newFormNumber}-protein" step="any" class="numberinput form-control" id="id_form-${newFormNumber}-protein" onchange="calculateCalories()">
        </div>
    </div>
    `;

    lastDiv.after(newDiv);
}; 

function removeItem() {
    var totalForms = parseInt(document.getElementById("id_form-TOTAL_FORMS").value);

    if (totalForms === 1) {
        var myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
    myModal.show();
    return;
    }

    var lastDiv = document.getElementsByClassName("row")[totalForms - 1];
    lastDiv.remove();

    var newFormNumber = totalForms;
    document.getElementById("id_form-TOTAL_FORMS").value = newFormNumber - 1 ;

    calculateCalories();
};

function calculateCalories() {
    var totalForms = parseInt(document.getElementById("id_form-TOTAL_FORMS").value);
    var calories = 0;

    for (var i = 0; i < totalForms; i++) {
        var fats = document.getElementById(`id_form-${i}-fats`).value;
        fats = 0 ? fats === "" : fats;
        var carbs = document.getElementById(`id_form-${i}-carbs`).value;
        carbs = 0 ? carbs === "" : carbs;
        var protein = document.getElementById(`id_form-${i}-protein`).value;
        protein = 0 ? protein === "" : protein;

        calories += (fats * 9) + (carbs * 4) + (protein * 4);
    }

    document.getElementById("id_calories").value = calories;
}

$(document).ready(function() {
    var totalForms = parseInt(document.getElementById("id_form-TOTAL_FORMS").value);
    for (var i = 0; i < totalForms; i++) {
        document.getElementById(`id_form-${i}-food`).addEventListener("change", calculateCalories);
        document.getElementById(`id_form-${i}-fats`).addEventListener("change", calculateCalories);
        document.getElementById(`id_form-${i}-carbs`).addEventListener("change", calculateCalories);
        document.getElementById(`id_form-${i}-protein`).addEventListener("change", calculateCalories);
    }
});
