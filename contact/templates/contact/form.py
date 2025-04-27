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
        <p class="contact-subtitle">
            We'd love to hear from you! Reach out through the form below or use our contact details.
        </p>
    </header>

    <!-- Contact Information -->
    <section class="contact-info-section">
        <h2 class="section-title">Our Contact Details</h2>
        <div class="contact-info-grid">
            <div class="contact-card">
                <h3 class="contact-card-title">Address</h3>
                <p class="contact-card-content">
                    Youth Connect Headquarters<br>123 Unity Lane, Nansana, Uganda
                </p>
            </div>

            <div class="contact-card">
                <h3 class="contact-card-title">Email</h3>
                <p class="contact-card-content">
                    <a href="mailto:youthconnectgroup2021@gmail.com" class="contact-link">
                        youthconnectgroup2021@gmail.com
                    </a>
                </p>
            </div>

            <div class="contact-card">
                <h3 class="contact-card-title">Phone</h3>
                <p class="contact-card-content">
                    <a href="tel:+256785767695" class="contact-link">+256785767695</a><br>
                    <a href="tel:+256703883767" class="contact-link">+256703883767</a><br>
                    <a href="tel:+256705197926" class="contact-link">+256705197926</a>
                </p>
            </div>
        </div>
    </section>

    <!-- Contact Form -->
    <section class="contact-form-section">
        <h2 class="section-title">Send Us a Message</h2>
        <form id="contactForm" method="POST" action="{% url 'contact:send' %}" novalidate>
            {% csrf_token %}

            {% if errors %}
                <div class="error-summary">
                    <p>Please fix the following errors:</p>
                    <ul>
                        {% for field, error in errors.items %}
                            <li><strong>{{ field }}:</strong> {{ error }}</li>
                        {% endfor %}
                    </ul>
                </div>
            {% endif %}

            <div class="form-group">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" id="name" name="name" class="form-input"
                       value="{{ request.POST.name }}" placeholder="Your name" required>
                {% if errors.name %}
                    <div class="form-error">{{ errors.name }}</div>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="email" class="form-label">Email Address</label>
                <input type="email" id="email" name="email" class="form-input"
                       value="{{ request.POST.email }}" placeholder="your.email@example.com" required>
                {% if errors.email %}
                    <div class="form-error">{{ errors.email }}</div>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="message" class="form-label">Your Message</label>
                <textarea id="message" name="message" class="form-textarea"
                          rows="6" placeholder="Type your message here..."
                          required maxlength="500">{{ request.POST.message }}</textarea>
                {% if errors.message %}
                    <div class="form-error">{{ errors.message }}</div>
                {% endif %}
            </div>

            <div class="form-actions">
                <button type="submit" class="btn-submit">Send Message</button>
            </div>
        </form>
    </section>
</main>

{% block scripts %}
<script src="{% static 'js/contact.js' %}"></script>
{% endblock %}
