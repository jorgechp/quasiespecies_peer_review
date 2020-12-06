import { Router } from '@angular/router';
import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, AbstractControl, Form } from '@angular/forms';
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

  loginFormGroup: FormGroup;
  registerFormGroup: FormGroup;
  passwordFormGroup: FormGroup;
  recoveryFormGroup: FormGroup;
  recoveryFormSecondStageGroup: FormGroup;

  isRecoveringPassword = false;
  isRecoveringPasswordFirstStep = true;

  hideLogin = true;
  hideSignUp = true;

  createUserSuscription: Subscription | undefined;
  loginSuscription: Subscription | undefined;
  recoveryUserSuscription: Subscription | undefined;
  recoveryUserSecondStageSuscription: Subscription | undefined;
  isLogged = true;

  private validatePasswords(group: FormGroup): null | object {
    const password = group.get('password1');
    const password2 = group.get('password2');


    if (password && password2){
      if (password.value.length < 5 || password2.value.length < 5){
        return { minimumLength: true };
      }
      if ( password.value === password2.value){
        return null;
      }else{
        return { notSame: true };
      }
    }else{
      return { notSame: true };
    }
  }

  constructor(private router: Router,
              private formBuilder: FormBuilder,
              private snackMessageService: SnackMessageService,
              private userService: UserService) {

    this.loginFormGroup = formBuilder.group({
      login_nick: new FormControl('', [Validators.required]),
      login_password: new FormControl('', [Validators.required])
    });

    this.passwordFormGroup = this.formBuilder.group({
      password1: ['', Validators.required],
      password2: ['', Validators.required]
    }, {validator: this.validatePasswords}
    );

    this.registerFormGroup = formBuilder.group({
      signup_nick: new FormControl('', [Validators.required]),
      signup_mail: new FormControl('', [Validators.required, Validators.email]),
      conditionsAgree: new FormControl('', [Validators.requiredTrue]),
      passwords: this.passwordFormGroup
   });

    this.recoveryFormGroup = formBuilder.group({
      recovery_nick: new FormControl('', [Validators.required]),
      recovery_mail: new FormControl('', [Validators.required, Validators.email])
    });

    this.recoveryFormSecondStageGroup = formBuilder.group({
      recovery_token: new FormControl('', [Validators.required]),
      passwords: this.passwordFormGroup
    });

  }

  ngOnInit(): void {}

  ngOnDestroy(): void {
    if (this.createUserSuscription !== undefined){
      this.createUserSuscription.unsubscribe();
    }
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
    if (this.recoveryUserSuscription !== undefined){
      this.recoveryUserSuscription.unsubscribe();
    }
    if (this.recoveryUserSecondStageSuscription !== undefined){
      this.recoveryUserSecondStageSuscription.unsubscribe();
    }
  }


  get login_form(): { [key: string]: AbstractControl; } { return this.loginFormGroup.controls; }
  get signup_form(): { [key: string]: AbstractControl; } { return this.registerFormGroup.controls; }
  get recovery_form(): { [key: string]: AbstractControl; } { return this.recoveryFormGroup.controls; }
  get recovery_second_stage_form(): { [key: string]: AbstractControl; } { return this.recoveryFormSecondStageGroup.controls; }
  get password_form(): FormGroup { return this.passwordFormGroup; }

  enterEvent(formName: string): void{
    if (formName === 'login' && this.loginFormGroup.valid){
      this.loginSubmit();
    }

    if (formName === 'signup' && this.registerFormGroup.valid){
      this.registerSubmit();
    }

    if (formName === 'recovery' && this.recoveryFormGroup.valid){
      if (this.isRecoveringPasswordFirstStep){
        this.recoverySubmit();
      }else{
        this.recoverySecondStageSubmit();
      }
    }
  }

  loginSubmit(): void{
    if (this.loginFormGroup.valid){
      const nick = this.loginFormGroup.get('login_nick');
      const password = this.loginFormGroup.get('login_password');

      if (nick && password){
        this.loginSuscription = this.userService.loginUser(nick.value, password.value).subscribe(
          (response: boolean) => {
            if (response){
              this.snackMessageService.notifyNewSnackMessage('Welcome, ' + nick.value + '!');
              this.router.navigateByUrl('/');
            }
          },
          (error) => {
            if (error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('You can\'t login because there already exists an active login. Please, logout.');
            }
            else if (error.status === 401){
              this.snackMessageService.notifyNewSnackMessage('Your login details are incorrect. Please, check your nick or your password.');
            }
           }
        );
      }
    }
  }

  registerSubmit(): void{
    if (this.registerFormGroup.valid){
      const nick = this.registerFormGroup.get('signup_nick');
      const mail = this.registerFormGroup.get('signup_mail');
      const password = this.passwordFormGroup.get('password1');

      if (nick && mail && password){
        this.createUserSuscription = this.userService.registerUser(nick.value, mail.value, password.value).subscribe(
          (response: NewUserInterface) => {
            if (response.id !== undefined){
              this.snackMessageService.notifyNewSnackMessage('Your user is now registered and now you can log in the system. Thanks!');              
            }
          },
          (error) => {
            if (error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('Ups!, this nickname is in use. Please, use a different one. Maybe you\'re trying to log in?');
            }
           }
        );
      }
    }
  }

  recoverySubmit(): void{
    if (this.recoveryFormGroup.valid){
      const nick = this.recoveryFormGroup.get('recovery_nick');
      const mail = this.recoveryFormGroup.get('recovery_mail');

      if (nick && mail){
        this.recoveryUserSuscription = this.userService.userRecoveryPassword(nick.value, mail.value).subscribe(
          (response: boolean) => {
              if (response){
                this.isRecoveringPasswordFirstStep = false;
              }
            },
            (error) => {
              if (error.status === 400){
                this.snackMessageService.notifyNewSnackMessage('The nickname or the user is not valid.');
              }
            }
        );
      }
    }
  }

  recoverySecondStageSubmit(): void{
    const token = this.recoveryFormSecondStageGroup.get('recovery_token');
    const password = this.passwordFormGroup.get('password1');

    if (token && password){
      this.recoveryUserSecondStageSuscription = this.userService.userRecoveryChangePassword(token.value, password.value).subscribe(
        (response: boolean) => {
            if (response){
              this.snackMessageService.notifyNewSnackMessage('OK!, you can use your new password from now on.');
              this.isRecoveringPasswordFirstStep = true;
              this.isRecoveringPassword = false;
            }
          },
          (error) => {
            if (error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('This token has expired, or is not valid.');
            }
          }
        )
    }
  }
}
