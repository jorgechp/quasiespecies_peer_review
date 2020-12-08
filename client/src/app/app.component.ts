import { Component, OnInit, OnDestroy  } from '@angular/core';
import {TranslateService} from '@ngx-translate/core';

import {MatSnackBar, MatSnackBarRef, TextOnlySnackBar} from '@angular/material/snack-bar';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { Subscription } from 'rxjs';
import { SnackBarConfiguration } from '@src/app/models/snackbar-config-interface';

const ENABLED_LANGUAGES = ['en', 'es'];
const DEFAULT_LANGUAGE = 'en';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{
  title = 'quasispecies-peer-review';
  snackServiceSuscription: Subscription | undefined;
  snackDissmisingSuscription: Subscription | undefined;
  snackDismissRequestSuscription: Subscription | undefined;
  snackBarRef: MatSnackBarRef<TextOnlySnackBar> | undefined;

  constructor(private translate: TranslateService,
              private snackBar: MatSnackBar,
              private snackService: SnackMessageService){
                translate.setDefaultLang(DEFAULT_LANGUAGE);
                const browserLanguage = translate.getBrowserCultureLang();
                if (ENABLED_LANGUAGES.includes(browserLanguage)){
                  translate.use(browserLanguage);
                }else{
                  translate.use(DEFAULT_LANGUAGE);
                }
              }

  ngOnInit(): void {

    this.snackServiceSuscription = this.snackService.subscribeSnackMessage().subscribe(
        (message: SnackBarConfiguration) => {
          if (message.time < 0 ){
            this.snackBarRef = this.snackBar.open(message.message, 'Close');
          }else{
            this.snackBarRef = this.snackBar.open(message.message, 'Close', {duration: message.time});
          }
          this.snackBarRef.afterDismissed().subscribe(
            () => {
              this.snackService.notifyDissmising();
            }
          );
      }
    );

    this.snackDismissRequestSuscription = this.snackService.subscribeDismissRequest().subscribe(
          () => {
            if (this.snackBarRef !== undefined){
              this.snackBarRef.dismiss();
            }
          }
    );
  }

  ngOnDestroy(): void {}

}
