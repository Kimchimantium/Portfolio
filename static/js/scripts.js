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
    .collapse:not(.show) .skill-content {
        position: relative;
        max-height: 100px; /* Adjust based on the desired preview height */
        overflow: hidden;
    }

    .collapse:not(.show) .skill-content::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 40px; /* Height of the fading effect */
        background: linear-gradient(transparent, #fff); /* Use your background color */
    }

    .collapse.show .skill-content::after {
        /* Remove the effect when expanded */
        display: none;
    }