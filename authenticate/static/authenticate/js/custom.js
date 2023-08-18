$(document).ready(function() {
    $('#chart_type').multiselect({
        nonSelectedText: 'Select Chart Type',
        buttonClass: 'form-control',
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        maxHeight: 200
    });
});
