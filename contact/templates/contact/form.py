{% extends 'base.html' %}
{% load static %}

{% block styles %}
<link href="{% static 'css/contact.css' %}" rel="stylesheet">
{% endblock %}

{% block title %}Contact Us | Youth Connect{% endblock %}

{% block content %}
<main class="contact-page">
    <!-- Notification System -->
    <div class="notification-container" aria-live="polite"></div>

    <!-- Page Header -->
    <header class="contact-header">
        <h1 class="contact-title">Contact Us</h1>
        <p class="contact-subtitle">We'd love to hear from you! Reach out through the form below or using our contact details.</p>
    </header>

    <!-- Contact Information -->
    <section class="contact-info-section">
        <h2 class="section-title">Our Contact Details</h2>
        <div class="contact-info-grid">
            <div class="contact-card">
                <div class="contact-card-icon">
                    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 11.5A2.5 2.5 0 0 1 9.5 9A2.5 2.5 0 0 1 12 6.5A2.5 2.5 0 0 1 14.5 9a2.5 2.5 0 0 1-2.5 2.5M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Z"/></svg>
                </div>
                <h3 class="contact-card-title">Address</h3>
                <p class="contact-card-content">Youth Connect Headquarters<br>123 Unity Lane, Nansana, Uganda</p>
                <button class="map-button" data-address="123 Unity Lane, Nansana, Uganda">View on Map</button>
            </div>

            <div class="contact-card">
                <div class="contact-card-icon">
                    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6m-2 0l-8 5l-8-5h16m0 12H4V8l8 5l8-5v10Z"/></svg>
                </div>
                <h3 class="contact-card-title">Email</h3>
                <p class="contact-card-content">
                    <a href="mailto:youthconnectgroup2021@gmail.com" class="contact-link">
                        youthconnectgroup2021@gmail.com
                    </a>
                </p>
            </div>

            <div class="contact-card">
                <div class="contact-card-icon">
                    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M6.62 10.79c1.44 2.83 3.76 5.15 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24c1.12.37 2.33.57 3.57.57c.55 0 1 .45 1 1V20c0 .55-.45 1-1 1c-9.39 0-17-7.61-17-17c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1c0 1.25.2 2.45.57 3.57c.11.35.03.74-.25 1.02l-2.2 2.2Z"/></svg>
                </div>
                <h3 class="contact-card-title">Phone</h3>
                <div class="contact-card-content">
                    <p><a href="tel:+256785767695" class="contact-link phone-number">+256785767695</a></p>
                    <p><a href="tel:+256703883767" class="contact-link phone-number">+256703883767</a></p>
                    <p><a href="tel:+256705197926" class="contact-link phone-number">+256705197926</a></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Form -->
    <section class="contact-form-section">
        <h2 class="section-title">Send Us a Message</h2>
        <form id="contactForm" method="POST" action="{% url 'contact:send' %}" novalidate>
            {% csrf_token %}

            <div class="form-group">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" id="name" name="name" class="form-input" placeholder="Your name" required
                       aria-describedby="name-error">
                <div class="form-error" id="name-error"></div>
            </div>

            <div class="form-group">
                <label for="email" class="form-label">Email Address</label>
                <input type="email" id="email" name="email" class="form-input" placeholder="your.email@example.com" required
                       aria-describedby="email-error">
                <div class="form-error" id="email-error"></div>
            </div>

            <div class="form-group">
                <label for="message" class="form-label">Your Message</label>
                <textarea id="message" name="message" class="form-textarea" rows="6"
                          placeholder="Type your message here..." required
                          aria-describedby="message-error message-counter" maxlength="500"></textarea>
                <div class="form-footer">
                    <div class="form-error" id="message-error"></div>
                    <div class="char-counter" id="message-counter">0/500 characters</div>
                </div>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn-submit">
                    <span class="btn-text">Send Message</span>
                    <span class="btn-loading">
                        <span class="btn-spinner"></span>
                        Sending...
                    </span>
                </button>
                <p class="form-disclaimer">
                    By submitting, you agree to our <a href="/privacy">privacy policy</a>.
                </p>
            </div>
        </form>
        <form id="contactForm" action="/contact/send/" method="post">
    {% if errors %}
        <ul class="error-list">
            {% for field, error in errors.items %}
                <li><strong>{{ field }}:</strong> {{ error }}</li>
            {% endfor %}
        </ul>
    {% endif %}
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Your Email" required>
    <textarea name="message" placeholder="Your Message" required></textarea>
    <button type="submit">Send</button>
</form>
    </section>

    <!-- Result Container (hidden by default) -->
    <div id="resultContainer" class="result-container hidden">
        <div class="result-icon">
            <svg viewBox="0 0 24 24"></svg>
        </div>
        <h2 class="result-title"></h2>
        <p class="result-message"></p>
        <button class="result-action">Continue</button>
    </div>
</main>

<!-- Map Modal (hidden by default) -->
<div id="mapModal" class="modal hidden">
    <div class="modal-content">
        <button class="modal-close" aria-label="Close map">&times;</button>
        <h3 class="modal-title">Our Location</h3>
        <div class="map-container">
            <!-- Map will be loaded here dynamically -->
            <div id="staticMap"></div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{% static 'js/contact.js' %}"></script>
{% endblock %}
