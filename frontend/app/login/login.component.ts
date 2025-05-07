import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-login',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  errorMessage = '';
  successMessage = '';

  login() {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter both email and password.';
      return;
    }

    // Dummy login logic
    if (this.email === 'admin@example.com' && this.password === 'admin') {
      this.successMessage = 'Login successful!';
      console.log('Logging in with', this.email);
    } else {
      this.errorMessage = 'Invalid credentials. Try again.';
    }
  }
}
