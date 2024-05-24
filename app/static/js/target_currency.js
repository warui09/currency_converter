/**
 * loads the form to display the drop down menu to select the target currency
 */

async function loadForm() {
  const response = await fetch('/templates/currencies_form.html');
  if (response.ok) {
    const formHtml = await response.text();
    document.getElementById('currency-form').innerHTML = formHtml;
    formHtml.setAttribute("id", "target_currency");
  } else {
    console.error('Failed to fetch currencies_form.html');
  }
}

window.onload = loadForm;
