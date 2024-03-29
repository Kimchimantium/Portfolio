/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})
document.addEventListener('DOMContentLoaded', function() {
            const creds = document.querySelector('.creds');
            const credMessage = document.querySelector('.cred-message');

            // Add event listeners for hover
            creds.addEventListener('mouseenter', () => {
                creds.classList.add('hovered');
                creds.classList.remove('not-hovered');
            });

            creds.addEventListener('mouseleave', () => {
                creds.classList.remove('hovered');
                creds.classList.add('not-hovered');
            });
});

document.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById("copyButton").addEventListener("click", function() {
    var emailText = document.getElementById("emailText").innerText;
    navigator.clipboard.writeText(emailText).then(function() {
      alert('Email copied to clipboard!');
    }, function(err) {
      console.error('Failed to copy: ', err);
      alert('Failed to copy text to clipboard');
    });
  });
});

document.getElementById('toggleLang').addEventListener('click', function() {
    var englishContent = document.getElementById('englishContent');
    var koreanContent = document.getElementById('koreanContent');
    if (englishContent.style.display === 'none') {
        englishContent.style.display = 'block';
        koreanContent.style.display = 'none';
    } else {
        englishContent.style.display = 'none';
        koreanContent.style.display = 'block';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const collapseElement = document.getElementById('collapseExample');
    const toggleButton = document.getElementById('toggleButton');
    const buttonIcon = toggleButton.querySelector('i'); // Assuming there's only one icon in the toggleButton

    // Convert jQuery event handling to vanilla JavaScript for Bootstrap 5
    collapseElement.addEventListener('show.bs.collapse', function () {
        console.log('Collapse is opening');
        toggleButton.innerHTML = 'Hide Skill Stacks <i class="fa-solid fa-caret-up"></i>';
        // If using classList for the icon, uncomment the next line
        // buttonIcon.classList.replace('fa-caret-up', 'fa-caret-down');
    });

    collapseElement.addEventListener('hide.bs.collapse', function () {
        console.log('Collapse is closing');
        toggleButton.innerHTML = 'Show Skill Stacks <i class="fa-solid fa-caret-down"></i>';
        // If using classList for the icon, uncomment the next line
        // buttonIcon.classList.replace('fa-caret-down', 'fa-caret-up');
    });
});
