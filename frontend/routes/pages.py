"""
Page rendering routes
"""

from flask import render_template, redirect, url_for, session


def register_page_routes(app):
    """Register all page routes"""
    
    @app.route('/')
    def index():
        """Render the project overview page as the landing page"""
        return render_template('overview.html')
    
    @app.route('/login')
    def login():
        """Render the login page"""
        return render_template('login.html')
    
    @app.route('/manager-dashboard')
    def manager_dashboard():
        """Render the manager dashboard (requires login)"""
        if 'manager_id' not in session:
            return redirect(url_for('index'))
        return render_template('manager_dashboard.html')
    
    @app.route('/employee')
    def employee():
        """Render the employee form (requires login)"""
        if 'employee_id' not in session:
            return redirect(url_for('index'))
        return render_template('form.html')
    
    @app.route('/check-exception-status', strict_slashes=False)
    def check_exception_status():
        """Render the check exception status page"""
        return render_template('check_exception_status.html')
