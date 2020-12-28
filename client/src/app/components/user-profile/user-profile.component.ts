import { Subscription } from 'rxjs';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { UserService } from '@src/app/services/user.service';
import { SnackMessageService } from '@src/app/services/snack-message.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit, OnDestroy {

  passwordFormGroup: FormGroup;
  newPasswordFormGroup: FormGroup;

  hidePassword = true;
  isLogged = false;
  
  passwordSubscription: Subscription | undefined;
  private loginSuscription: Subscription | undefined;

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


  constructor(private formBuilder: FormBuilder,
              private userService: UserService,
              private snackMessageService: SnackMessageService) {

    this.newPasswordFormGroup = this.formBuilder.group({
        password1: ['', Validators.required],
        password2: ['', Validators.required]
      }, {validator: this.validatePasswords}
    );

    this.passwordFormGroup = this.formBuilder.group({
      currentPassword: new FormControl('', [Validators.required]),
      passwords: this.newPasswordFormGroup
    });
  }

  ngOnInit(): void { 
    this.subscribeCheckLogin();
  }

  ngOnDestroy(): void {
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
  }

  get password_form(): { [key: string]: AbstractControl; } { return this.passwordFormGroup.controls; }
  get new_password_form(): FormGroup { return this.newPasswordFormGroup; }

  subscribeCheckLogin(): void{
    this.loginSuscription = this.userService.checkLogin().subscribe(
      (isLogged: boolean) => {
        this.isLogged = isLogged;
      }
    );
  }

  enterEvent(eventType: string): void{
    switch (eventType){
      case 'password':
        this.changePassword();
        break;
    }
  }

  changePassword(): void {
    if (this.passwordFormGroup.valid){
      const currentPassword = this.passwordFormGroup.get('currentPassword');
      const password1 = this.newPasswordFormGroup.get('password1');
      const password2 = this.newPasswordFormGroup.get('password2');

      if (currentPassword && password1 && password2 && password2.value === password2.value){
        this.passwordSubscription = this.userService.userChangePassword(currentPassword.value, password1.value).subscribe(
          (response: boolean) => {
            if (response){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_PASSWORD_OK');
            }else{
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_PASSWORD_FAILED');
            }
          }
        );
      }
    }
  }

}
