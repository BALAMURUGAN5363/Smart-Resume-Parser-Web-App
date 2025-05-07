import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LoginComponent],
      imports: [FormsModule] // Needed for ngModel
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should have empty email and password initially', () => {
    expect(component.email).toBe('');
    expect(component.password).toBe('');
  });

  it('should call login and log the email/password', () => {
    spyOn(console, 'log');
    component.email = 'user@example.com';
    component.password = 'secret';
    component.login();
    expect(console.log).toHaveBeenCalledWith('Logging in with', 'user@example.com', 'secret');
  });
});
