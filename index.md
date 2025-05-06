<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alireza Eftekhari | Marine Renewable Energy Research</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --primary: #1e88e5;
      --secondary: #26a69a;
      --dark: #212121;
      --light: #f5f5f5;
      --accent: #ff7043;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
      background-color: var(--light);
      color: var(--dark);
      line-height: 1.6;
    }
    
    /* Navigation */
    .navbar {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .navbar h1 {
      font-size: 1.5rem;
      font-weight: 600;
    }
    
    .nav-links {
      display: flex;
      list-style: none;
    }
    
    .nav-links li {
      margin-left: 1.5rem;
    }
    
    .nav-links a {
      color: white;
      text-decoration: none;
      transition: color 0.3s;
    }
    
    .nav-links a:hover {
      color: var(--accent);
    }
    
    /* Hero Section */
    .hero {
      background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('/api/placeholder/1200/400');
      background-size: cover;
      background-position: center;
      height: 40vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      color: white;
      padding: 0 2rem;
    }
    
    .hero h2 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    
    .hero p {
      font-size: 1.2rem;
      max-width: 800px;
    }
    
    /* Main Content */
    .container {
      max-width: 1200px;
      margin: 2rem auto;
      padding: 0 2rem;
    }
    
    .section {
      margin-bottom: 3rem;
    }
    
    .section-header {
      display: flex;
      align-items: center;
      margin-bottom: 1.5rem;
      border-bottom: 3px solid var(--primary);
      padding-bottom: 0.5rem;
    }
    
    .section-header i {
      font-size: 1.5rem;
      color: var(--primary);
      margin-right: 0.5rem;
    }
    
    .section-header h3 {
      font-size: 1.8rem;
      font-weight: 600;
    }
    
    /* Project Cards */
    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
    }
    
    .project-card {
      background-color: white;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      transition: transform 0.3s;
    }
    
    .project-card:hover {
      transform: translateY(-5px);
    }
    
    .project-img {
      height: 160px;
      background-color: var(--primary);
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
      font-size: 3rem;
    }
    
    .project-content {
      padding: 1.5rem;
    }
    
    .project-content h4 {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
    }
    
    .project-content p {
      margin-bottom: 1rem;
      color: #666;
    }
    
    .project-links {
      display: flex;
      justify-content: space-between;
    }
    
    .project-links a {
      text-decoration: none;
      color: var(--primary);
      font-weight: 600;
      transition: color 0.3s;
    }
    
    .project-links a:hover {
      color: var(--accent);
    }
    
    /* Profile Section */
    .profile {
      display: flex;
      align-items: center;
      gap: 2rem;
      margin-bottom: 2rem;
    }
    
    .profile-img {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      background-color: var(--secondary);
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
      font-size: 3rem;
      flex-shrink: 0;
    }
    
    .profile-content {
      flex-grow: 1;
    }
    
    .profile-content h3 {
      font-size: 1.8rem;
      margin-bottom: 0.5rem;
    }
    
    .profile-content p {
      margin-bottom: 1rem;
    }
    
    .social-links {
      display: flex;
      gap: 1rem;
    }
    
    .social-links a {
      display: inline-flex;
      justify-content: center;
      align-items: center;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: var(--primary);
      color: white;
      text-decoration: none;
      transition: background-color 0.3s;
    }
    
    .social-links a:hover {
      background-color: var(--accent);
    }
    
    /* Footer */
    footer {
      background-color: var(--dark);
      color: white;
      text-align: center;
      padding: 2rem;
      margin-top: 3rem;
    }
    
    footer p {
      margin-bottom: 1rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
      .profile {
        flex-direction: column;
        text-align: center;
      }
      
      .social-links {
        justify-content: center;
      }
      
      .projects-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <!-- Navigation -->
  <nav class="navbar">
    <h1>Alireza Eftekhari</h1>
    <ul class="nav-links">
      <li><a href="#about">About</a></li>
      <li><a href="#projects">Projects</a></li>
      <li><a href="#publications">Publications</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>
  
  <!-- Hero Section -->
  <div class="hero">
    <h2>Marine Renewable Energy Research</h2>
    <p>Exploring tidal, wave, wind, and solar resources with a focus on their complementarity and predictability</p>
  </div>
  
  <!-- Main Content -->
  <div class="container">
    <!-- About Section -->
    <section id="about" class="section">
      <div class="section-header">
        <i class="fas fa-user"></i>
        <h3>About Me</h3>
      </div>
      <div class="profile">
        <div class="profile-img">
          <i class="fas fa-user"></i>
        </div>
        <div class="profile-content">
          <h3>Alireza Eftekhari</h3>
          <p>I'm a researcher specializing in marine renewable energy and climate change impacts. I use high-resolution hydrodynamic models to assess tidal, wave, wind, and solar resources, with a focus on their complementarity and predictability.</p>
          <p>My work includes identifying viable tidal energy sites, simulating estuarine and coastal processes, and analyzing the effects of climate change on marine resource availability. I'm experienced with modeling tools like CROCO, DHI MIKE, and DIVAST, and I regularly work on HPC systems using parallel programming to run and analyze large-scale simulations.</p>
          <div class="social-links">
            <a href="https://github.com/eftekhari-alireza" target="_blank"><i class="fab fa-github"></i></a>
            <a href="https://scholar.google.com/citations?user=_Bobmm4AAAAJ&hl=en&oi=ao" target="_blank"><i class="fas fa-graduation-cap"></i></a>
            <a href="https://www.researchgate.net/profile/Alireza-Eftekhari-4?ev=hdr_xprf" target="_blank"><i class="fab fa-researchgate"></i></a>
            <a href="mailto:your.email@example.com"><i class="fas fa-envelope"></i></a>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Projects Section -->
    <section id="projects" class="section">
      <div class="section-header">
        <i class="fas fa-flask"></i>
        <h3>Research Projects</h3>
      </div>
      <div class="projects-grid">
        <!-- Project 1 -->
        <div class="project-card">
          <div class="project-img">
            <i class="fas fa-water"></i>
          </div>
          <div class="project-content">
            <h4>Shannon Estuary Tidal Modeling</h4>
            <p>Comprehensive tidal energy assessment using advanced hydrodynamic modeling techniques.</p>
            <div class="project-links">
              <a href="#">Coming Soon</a>
              <a href="#"><i class="fas fa-arrow-right"></i></a>
            </div>
          </div>
        </div>
        
        <!-- Project 2 -->
        <div class="project-card">
          <div class="project-img">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="project-content">
            <h4>Tidal Harmonic Analysis</h4>
            <p>Developing tools and methodologies for accurate tidal data analysis and prediction.</p>
            <div class="project-links">
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Tidal-Harmonic-Analysis">View Project</a>
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Tidal-Harmonic-Analysis"><i class="fas fa-arrow-right"></i></a>
            </div>
          </div>
        </div>
        
        <!-- Project 3 -->
        <div class="project-card">
          <div class="project-img">
            <i class="fas fa-plug"></i>
          </div>
          <div class="project-content">
            <h4>Tidal Power Curve Analysis</h4>
            <p>Evaluating energy extraction potential from various tidal power technologies.</p>
            <div class="project-links">
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/tidal-power-curve">View Project</a>
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/tidal-power-curve"><i class="fas fa-arrow-right"></i></a>
            </div>
          </div>
        </div>
        
        <!-- Project 4 -->
        <div class="project-card">
          <div class="project-img">
            <i class="fas fa-cloud-showers-heavy"></i>
          </div>
          <div class="project-content">
            <h4>Storm Surge Detection Model</h4>
            <p>Predicting and modeling surge events for coastal safety and infrastructure planning.</p>
            <div class="project-links">
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model">View Project</a>
              <a href="https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model"><i class="fas fa-arrow-right"></i></a>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Publications Section -->
    <section id="publications" class="section">
      <div class="section-header">
        <i class="fas fa-book"></i>
        <h3>Publications & Research</h3>
      </div>
      <p>You can find my complete list of publications on my academic profiles:</p>
      <ul style="list-style-type: none; margin-top: 1rem;">
        <li style="margin-bottom: 0.5rem;"><i class="fas fa-graduation-cap" style="color: var(--primary); margin-right: 0.5rem;"></i> <a href="https://scholar.google.com/citations?user=_Bobmm4AAAAJ&hl=en&oi=ao" style="color: var(--primary); text-decoration: none;">Google Scholar</a></li>
        <li><i class="fab fa-researchgate" style="color: var(--primary); margin-right: 0.5rem;"></i> <a href="https://www.researchgate.net/profile/Alireza-Eftekhari-4?ev=hdr_xprf" style="color: var(--primary); text-decoration: none;">ResearchGate</a></li>
      </ul>
    </section>
    
    <!-- Contact Section -->
    <section id="contact" class="section">
      <div class="section-header">
        <i class="fas fa-envelope"></i>
        <h3>Contact</h3>
      </div>
      <p>If you're interested in collaboration or have any questions about my research, don't hesitate to reach out!</p>
      <div style="margin-top: 1rem;">
        <p><i class="fas fa-envelope" style="color: var(--primary); margin-right: 0.5rem;"></i> Email: <a href="mailto:your.email@example.com" style="color: var(--primary); text-decoration: none;">your.email@example.com</a></p>
        <p><i class="fas fa-file-pdf" style="color: var(--primary); margin-right: 0.5rem;"></i> <a href="assets/pdf/Alireza_Eftekhari_CV.pdf" style="color: var(--primary); text-decoration: none;">Download my Resume (PDF)</a></p>
      </div>
    </section>
  </div>
  
  <!-- Footer -->
  <footer>
    <p>&copy; 2025 Alireza Eftekhari. All rights reserved.</p>
    <div>
      <a href="https://github.com/eftekhari-alireza" style="color: white; margin: 0 0.5rem;"><i class="fab fa-github"></i></a>
      <a href="https://scholar.google.com/citations?user=_Bobmm4AAAAJ&hl=en&oi=ao" style="color: white; margin: 0 0.5rem;"><i class="fas fa-graduation-cap"></i></a>
      <a href="https://www.researchgate.net/profile/Alireza-Eftekhari-4?ev=hdr_xprf" style="color: white; margin: 0 0.5rem;"><i class="fab fa-researchgate"></i></a>
    </div>
  </footer>
</body>
</html>
