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
  mailFormGroup: FormGroup;
  roleFormGroup: FormGroup;

  currentMail = '';
  currentPasswordValue = '';
  hidePassword = true;
  isLogged = false; 
  isDeleteConfirmationVisible = false;
  
  private passwordSubscription: Subscription | undefined;
  private loginSuscription: Subscription | undefined;
  private userMailSuscription: Subscription | undefined;
  private roleSuscription: Subscription | undefined;
  private roleRetrieveSuscription: Subscription | undefined;
  private deleteAccountSuscription: Subscription | undefined;

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

  private createMailFormGroup(value: string): void{
    this.mailFormGroup = this.formBuilder.group({      
      mail: new FormControl(value, [Validators.required, Validators.email]),
    });
  }

  private createRolesFormGroup(isEditor: boolean, isReviewer: boolean): void{
    this.roleFormGroup = this.formBuilder.group({      
      im_editor: new FormControl(isEditor),
      im_reviewer: new FormControl(isReviewer),
    });   
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
      passwords: this.newPasswordFormGroup
    });

    this.mailFormGroup = this.formBuilder.group({      
      mail: new FormControl('', [Validators.required, Validators.email]),
    });    

    this.roleFormGroup = this.formBuilder.group({      
      im_editor: new FormControl(''),
      im_reviewer: new FormControl(''),
    });   
  }

  ngOnInit(): void { 
    this.subscribeCheckLogin();
    this.subscribeUserMail();
    this.subscribeUserRoles();
  }

  ngOnDestroy(): void {
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
    if (this.passwordSubscription !== undefined){
      this.passwordSubscription.unsubscribe();
    }
    if (this.userMailSuscription !== undefined){
      this.userMailSuscription.unsubscribe();
    }
    if (this.roleSuscription !== undefined){
      this.roleSuscription.unsubscribe();
    }
    if (this.roleRetrieveSuscription !== undefined){
      this.roleRetrieveSuscription.unsubscribe();
    }   
    if (this.deleteAccountSuscription !== undefined){
      this.deleteAccountSuscription.unsubscribe();
    }
  }

  get password_form(): { [key: string]: AbstractControl; } { return this.passwordFormGroup.controls; }
  get mail_form(): { [key: string]: AbstractControl; }  { return this.mailFormGroup.controls; }
  get new_password_form(): FormGroup { return this.newPasswordFormGroup; }

  subscribeUserMail(): void{
    this.userMailSuscription = this.userService.userMail().subscribe(
      (mail: string) => {
        this.currentMail = mail;
        this.createMailFormGroup(mail);
      }
    );
  }

  subscribeUserRoles(): void{
    this.roleRetrieveSuscription = this.userService.getUserRole().subscribe(
      (roles: Array<string>) => {
        const isEditor = roles.includes('editor');
        const isReviewer = roles.includes('reviewer');
        this.createRolesFormGroup(isEditor, isReviewer);
      }
    );
  }

  subscribeCheckLogin(): void{
    this.loginSuscription = this.userService.checkLogin().subscribe(
      (isLogged: boolean) => {
        this.isLogged = isLogged;
      }
    );
  }

  enterEvent(eventType: string): void{
    const a = this.mailFormGroup;
    if(this.currentPasswordValue.length > 0){
      switch (eventType){
        case 'password':          
          this.changePassword();
          break;
        case 'mail':
          this.changeMail();
          break;
        case 'role':
          this.changeRole();
          break;
      }
    }
  }

  changePassword(): void {
    if (this.passwordFormGroup.valid){      
      const password1 = this.newPasswordFormGroup.get('password1');
      const password2 = this.newPasswordFormGroup.get('password2');

      if (this.currentPasswordValue && password1 && password2 && this.currentPasswordValue.length > 0 && password2.value === password2.value){
        this.passwordSubscription = this.userService.userChangePassword(this.currentPasswordValue, password1.value).subscribe(
          (response: boolean) => {
            if (response){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_PASSWORD_OK');
            }else{
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_PASSWORD_FAILED');
            }
          },(error) => {
            if (error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.ERROR_DATA');
            }
            else if (error.status === 401){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.NOT_AUTHORIZED');
            }
          }
        );
      }
    }
  }

  changeMail(): void {
    if (this.mailFormGroup !== undefined && this.mailFormGroup.valid){      
      const newMail = this.mailFormGroup.get('mail');

      if (this.currentPasswordValue && newMail && this.currentPasswordValue.length > 0 && newMail.value != this.currentMail){
        this.passwordSubscription = this.userService.userChangeMail(this.currentPasswordValue, newMail.value).subscribe(
          (response: boolean) => {
            if (response){
              this.currentMail = newMail.value;
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_MAIL_OK');
            }else{
              this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_MAIL_FAILED');
            }
          },(error) => {
            if (error.status === 400){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.ERROR_DATA');
            }
            else if (error.status === 401){
              this.snackMessageService.notifyNewSnackMessage('PROFILE.NOT_AUTHORIZED');
            }
          }
        );
      }
    }
  }

  changeRole(): void {
    const imEditor = this.roleFormGroup.value.im_editor;
    const imReviewer = this.roleFormGroup.value.im_reviewer;

    this.roleSuscription = this.userService.userChangeRole(this.currentPasswordValue, imEditor, imReviewer).subscribe(
      (response: boolean) => {
        if(response){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_ROLE_OK');
        }else{
          this.snackMessageService.notifyNewSnackMessage('PROFILE.CHANGE_ROLE_FAILED');
        }
      },(error) => {
        if (error.status === 400){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.ERROR_DATA');
        }
        else if (error.status === 401){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.NOT_AUTHORIZED');
        }
      }
    );
  }

  deleteAccount(): void{
    this.deleteAccountSuscription = this.userService.deleteAccount(this.currentPasswordValue).subscribe(
      (response: boolean) => {
        if(response){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.DELETE_OK');
          this.isLogged = false;
        }else{
          this.snackMessageService.notifyNewSnackMessage('PROFILE.DELETE_FAILED');
        }
      },(error) => {
        if (error.status === 400){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.ERROR_DATA');
        }
        else if (error.status === 401){
          this.snackMessageService.notifyNewSnackMessage('PROFILE.NOT_AUTHORIZED');
        }
      }
    );
  }

}
