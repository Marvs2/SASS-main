const api_base_url = '{{ faculty_api_base_url | default("") }}';

async function fetchFacultyId() {
  try {
    const response = await fetch(`${api_base_url}/faculty-id`);
    console.log('Fetching:', `${api_base_url}/faculty-id`);
    if (!response.ok) {
      throw new Error(`Failed to fetch data. Server returned ${response.status}`);
    }
    const data_faculty_id = await response.json();
    console.log('Faculty ID Data:', data_faculty_id); // Debugging
    displayFacultyOptions(data_faculty_id.FacultyId);
  } catch (error) {
    console.error('Error fetching faculty ID:', error.message);
  }
}

function displayFacultyOptions(facultyId) {
  const manageServicesMenu = document.getElementById('manageServicesMenu');
  if (manageServicesMenu) {
    let optionsHTML = '<ul>';

    if (facultyId === 10017) {
      optionsHTML += `
        <li><a href="{{ url_for('facultyoverload') }}">Overload of Subjects</a></li>
        <li><a href="{{ url_for('facultypetition') }}">Online Petition of Subjects</a></li>
        <li><a href="{{ url_for('facultyshifting') }}">Application for Shifting</a></li>
        <li><a href="{{ url_for('facultytutorial') }}">Online Request for Tutorial</a></li>
      `;
    } else if (facultyId === 10018) {
      optionsHTML += `
        <li><a href="{{ url_for('facultyadding') }}">Adding of Subjects</a></li>
        <li><a href="{{ url_for('facultychange') }}">Change of Schedule/Subjects</a></li>
        <li><a href="{{ url_for('facultycrossenrollment') }}">Cross-Enrollment</a></li>
      `;
    } else if (facultyId === 1) {
      optionsHTML += `
        <li><a href="{{ url_for('facultycorrection') }}">Correction of Grade Entry</a></li>
        <li><a href="{{ url_for('facultyenrollment') }}">Manual Enrollment</a></li>
        <li><a href="{{ url_for('facultycertification') }}">Request for Certification</a></li>
      `;
    } else {
      optionsHTML += `
        <li><a href="{{ url_for('facultyoverload') }}">Overload of Subjects</a></li>
        <li><a href="{{ url_for('facultypetition') }}">Online Petition of Subjects</a></li>
        <li><a href="{{ url_for('facultyshifting') }}">Application for Shifting</a></li>
        <li><a href="{{ url_for('facultytutorial') }}">Online Request for Tutorial</a></li>
        <li><a href="{{ url_for('facultyadding') }}">Adding of Subjects</a></li>
        <li><a href="{{ url_for('facultychange') }}">Change of Schedule/Subjects</a></li>
        <li><a href="{{ url_for('facultycrossenrollment') }}">Cross-Enrollment</a></li>
        <li><a href="{{ url_for('facultycorrection') }}">Correction of Grade Entry</a></li>
        <li><a href="{{ url_for('facultyenrollment') }}">Manual Enrollment</a></li>
        <li><a href="{{ url_for('facultycertification') }}">Request for Certification</a></li>
      `;
    }

    optionsHTML += '</ul>';
    manageServicesMenu.innerHTML = optionsHTML;
    console.log('manageServicesMenu HTML:', optionsHTML); // Debugging
  } else {
    console.error('manageServicesMenuElement is null');
  }
}

fetchFacultyId();