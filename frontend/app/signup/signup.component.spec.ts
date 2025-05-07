import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SignupComponent } from './signup.component';

describe('SignupComponent', () => {
  let component: SignupComponent;
  let fixture: ComponentFixture<SignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SignupComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy(); // Test passes if component is created successfully
  });

  it('should initialize email and password as empty strings', () => {
    expect(component.email).toBe('');
    expect(component.password).toBe('');
  });

  it('should call signup method', () => {
    spyOn(console, 'log');
    component.email = 'test@example.com';
    component.password = 'password123';
    component.signup();
    expect(console.log).toHaveBeenCalledWith('Signing up with', 'test@example.com', 'password123');
  });
});
