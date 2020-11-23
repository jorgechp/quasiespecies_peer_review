import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, AbstractControl } from '@angular/forms';
import { Validators } from '@angular/forms';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  loginForm: FormGroup;
  registerForm: FormGroup;

  hide = true;

  constructor(private formBuilder: FormBuilder) {
    this.loginForm = formBuilder.group({
      login_nick: new FormControl('', [Validators.required]),
      login_password: new FormControl('', [Validators.required])
    });

    this.registerForm = formBuilder.group({
      signup_nick: new FormControl('', [Validators.required]),
      signup_mail: new FormControl('', [Validators.required, Validators.email]),
      signup_password: new FormControl('', [Validators.required]),
      signup_password2: new FormControl('', [Validators.required])
    });
   }

  ngOnInit(): void {}

  get login_form() { return this.loginForm.controls; }
  get signup_form() { return this.registerForm.controls; }

  loginSubmit(): void{
    
  }

  registerSubmit(): void{

  }

}
