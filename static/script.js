document.addEventListener("DOMContentLoaded", function() {
  const searchBox = document.getElementById('searchBox');
  const searchBtn = document.getElementById('searchBtn');
  const suggestionList = document.getElementById('suggestionList');
  const countrySelect = document.getElementById('country');

  searchBox.addEventListener('input', searchDrugs);
  searchBtn.addEventListener('click', searchDrugs);
  countrySelect.addEventListener('change', searchDrugs);
});

function searchDrugs() {
  const query = document.getElementById('searchBox').value;
  const country = document.getElementById('country').value;
  const list = document.getElementById('suggestionList');
  list.innerHTML = '';
  if (query.length === 0) return;
  let url = `/search?q=${encodeURIComponent(query)}`;
  if (country) url += `&country=${encodeURIComponent(country)}`;
  fetch(url)
    .then(r => r.json())
    .then(drugs => {
      drugs.forEach(drug => {
        const li = document.createElement('li');
        li.textContent = drug;
        li.onclick = () => showDrugDetail(drug);
        list.appendChild(li);
      });
    });
}

function showDrugDetail(name) {
  fetch(`/drug_detail?name=${encodeURIComponent(name)}`)
    .then(r => r.json())
    .then(detail => {
      if (detail.error) {
        document.getElementById('detailTitle').textContent = 'Not found';
        document.getElementById('props').innerHTML = '';
        return;
      }
      // Accept both uppercase and lowercase keys for drug name
      const drugName = detail['drug_name'] || detail['DRUG_NAME'] || 'No Name';
      document.getElementById('detailTitle').textContent = drugName;
      let html = '';
      for (const [key, value] of Object.entries(detail)) {
        html += `<div><strong>${key.replace(/_/g, ' ')}:</strong> ${value}</div>`;
      }
      document.getElementById('props').innerHTML = html;
      // Optionally update the country dropdown to match this drug's country
      if ('availability_country' in detail) {
        document.getElementById('country').value = detail['availability_country'];
      } else if ('AVAILABILITY_COUNTRY' in detail) {
        document.getElementById('country').value = detail['AVAILABILITY_COUNTRY'];
      }
    });
}
