import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, AbstractControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import { NewUserInterface } from '@src/app/models/new-user-interface.model';
import { SnackMessageService } from '@src/app/services/snack-message.service';
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

  createUserSuscription: Subscription | undefined;

  private matchValidator(group: FormGroup): boolean {
    const password = group.get('password1');
    const password2 = group.get('password2');

    if (password && password2){
      if(password.value === password2.value){
        return false;
      }else{
        return true;
      }
    }else{
      return false;
    }
  }

  constructor(private formBuilder: FormBuilder,
              private snackMessageService: SnackMessageService,
              private userService: UserService) {

    this.loginForm = formBuilder.group({
      login_nick: new FormControl('', [Validators.required]),
      login_password: new FormControl('', [Validators.required])
    });

    this.registerForm = formBuilder.group({
      signup_nick: new FormControl('', [Validators.required]),
      signup_mail: new FormControl('', [Validators.required, Validators.email]),
      passwords: this.formBuilder.group({
        password1: ['s', Validators.required],
        password2: ['s', Validators.required]
      }, {validator: this.matchValidator}
      )
    });
   }

  ngOnInit(): void {}
  ngOnDestroy(): void {
    if (this.createUserSuscription !== undefined){
      this.createUserSuscription.unsubscribe();
    }
  }

  get login_form() { return this.loginForm.controls; }
  get signup_form() { return this.registerForm.controls; }

  loginSubmit(): void{
    if (this.loginForm.valid){
      console.log('test');
    }
  }

  registerSubmit(): void{
    if (this.registerForm.valid){

      const username = this.registerForm.get('signup_nick');
      const nick = this.registerForm.get('signup_nick');
      const mail = this.registerForm.get('signup_mail');
      const password = this.registerForm.get('signup_password');

      if (username && nick && mail && password){
        this.createUserSuscription = this.userService.registerUser(nick.value, mail.value, password.value).subscribe(
          (response: NewUserInterface) => {
            if (response.id !== undefined){
              this.snackMessageService.notifyNewSnackMessage('Your user is now registered and now you can log in the system. Thanks!');
            }
          },
          (error) => {
            if(error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('Ups!, this nickname is in use. Please, use a different one. Maybe you\'re trying to log in?');
            }
           }
        );
      }
    }

  }

}
