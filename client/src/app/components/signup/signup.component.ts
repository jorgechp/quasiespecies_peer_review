import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, AbstractControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import { UserService } from '@src/app/services/user.service';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit, OnDestroy {

  loginForm: FormGroup;
  registerForm: FormGroup;

  hide = true;

  createUserSuscription: Subscription;

  constructor(private formBuilder: FormBuilder,
              private _userService: UserService) {
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
  ngOnDestroy(): void {
    this.createUserSuscription.unsubscribe();
  }

  get login_form() { return this.loginForm.controls; }
  get signup_form() { return this.registerForm.controls; }

  loginSubmit(): void{
    if(this.loginForm.valid){
      console.log('test');
    }
  }

  registerSubmit(): void{
    if(this.registerForm.valid){

      const username = this.registerForm.get('signup_nick');
      const nick = this.registerForm.get('signup_nick');
      const mail = this.registerForm.get('signup_mail');
      const password = this.registerForm.get('signup_password');

      if (username && nick && mail && password){
        this.createUserSuscription = this._userService.registerUser(nick.value, mail.value, password.value).subscribe(
          (response: object) => {
            console.log(response);
          }
        );
      }
    }

  }

}
