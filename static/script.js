  // Mobile menu toggle
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.querySelector('.menu-icon');

  mobileMenuButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      // Animate menu icon
      if (mobileMenu.classList.contains('hidden')) {
          menuIcon.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
      } else {
          menuIcon.setAttribute('d', 'M6 18L18 6M6 6l12 12');
      }
  });

  // Mobile dropdowns
  const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');
  mobileDropdowns.forEach(dropdown => {
      const button = dropdown.querySelector('button');
      const content = dropdown.querySelector('div');
      
      button.addEventListener('click', () => {
          content.classList.toggle('hidden');
          // Animate the dropdown
          if (!content.classList.contains('hidden')) {
              content.style.animation = 'slideDown 0.3s ease forwards';
          }
      });
  });

  // Close mobile menu when clicking outside
  document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target) && !mobileMenu.classList.contains('hidden')) {
          mobileMenu.classList.add('hidden');
          menuIcon.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
      }
  });

  window.addEventListener('load', function() {
    var video = document.getElementById('preload-video');
    var content = document.getElementById('content');
    var preloader = document.getElementById('preloader');
  
    // When the video ends, hide the preloader and show the content
    video.onended = function() {
      // Hide the preloader video
      preloader.style.display = 'none';
      
      // Show the main content
      content.style.display = 'block';
      setTimeout(function() {
        content.style.opacity = '1'; // Optional fade-in effect
      }, 100); // Delay for smooth transition
    };
  });

  window.addEventListener('load', function() {
    var video = document.getElementById('preload-video');
    var content = document.getElementById('content');
    var preloader = document.getElementById('preloader');
  
    // When the video ends, hide the preloader and show the content with transition
    video.onended = function() {
      // Hide the preloader video
      preloader.style.display = 'none';
      
      // Show the main content with sliding effect
      content.style.display = 'block';
      setTimeout(function() {
        content.classList.add('slide-in');
      }, 100); // Delay to apply the class after content is visible
    };
  });
  
  
  