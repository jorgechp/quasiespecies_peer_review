import { TranslateService } from '@ngx-translate/core';
import { NgcCookieConsentService, NgcStatusChangeEvent } from 'ngx-cookieconsent';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from '@src/app/services/user.service';
import { Subscription } from 'rxjs';
import {Router} from '@angular/router';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { CONFIG } from '@src/app/config';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {

  logoutSuscription: Subscription | undefined;
  private cookiesStatusChangeSubscription: Subscription | undefined;
  private loginSuscription: Subscription | undefined;

  isLogged = false;
  isAcceptedCookies = true;
  currentLanguage: string;

  constructor(private ccService: NgcCookieConsentService,
              private router: Router,
              private translateService: TranslateService,
              private snackMessageService: SnackMessageService,
              private userService: UserService) {
                this.currentLanguage = translateService.currentLang;
              }

  ngOnInit(): void {
    this.cookiesStatusChangeSubscription = this.ccService.statusChange$.subscribe(
      (event: NgcStatusChangeEvent) => {
        this.isAcceptedCookies = event.status === 'allow';
      });
    this.subscribeCheckLogin();
  }

  ngOnDestroy(): void {
    if (this.cookiesStatusChangeSubscription !== undefined){
      this.cookiesStatusChangeSubscription.unsubscribe();
    }
    if (this.logoutSuscription !== undefined){
      this.logoutSuscription.unsubscribe();
    }
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
  }

  subscribeCheckLogin(): void{
    this.loginSuscription = this.userService.getIsLoggedInObservable().subscribe(
      (isLogged: boolean) => {
        this.isLogged = isLogged;
      }
    );
  }

  doLogout(): void{
    this.logoutSuscription = this.userService.logout().subscribe(
      () => {
        console.log('Logout');
        this.snackMessageService.notifyNewSnackMessage(this.translateService.instant('SNACK.HEADER_LOGOUT'));
        this.router.navigateByUrl('/');
      }
    );
  }

  changeLanguage(newLanguage: string): void{
    console.log(CONFIG.VALID_LANGUAGES);
    if (CONFIG.VALID_LANGUAGES.includes(newLanguage)){
      const userLanguageSuscription = this.userService.setUserLanguage(newLanguage).subscribe(
        (response: boolean) => {
          if (response){
            this.translateService.use(newLanguage);
            this.currentLanguage = newLanguage;
          }
          userLanguageSuscription.unsubscribe();
        }
      );
    }
  }
}
