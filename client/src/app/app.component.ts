import { Component, OnInit, OnDestroy  } from '@angular/core';
import {MatSnackBar, MatSnackBarRef, TextOnlySnackBar} from '@angular/material/snack-bar';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { Subscription } from 'rxjs';
import { SnackBarConfiguration } from '@src/app/models/snackbar-config-interface';

import { NgcCookieConsentService, NgcInitializeEvent, NgcNoCookieLawEvent, NgcStatusChangeEvent } from 'ngx-cookieconsent';

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

  private popupOpenSubscription: Subscription | undefined;
  private popupCloseSubscription: Subscription | undefined;
  private initializeSubscription: Subscription | undefined;
  private statusChangeSubscription: Subscription | undefined ;
  private revokeChoiceSubscription: Subscription | undefined;
  private noCookieLawSubscription: Subscription | undefined;

  constructor(private ccService: NgcCookieConsentService,
              private snackBar: MatSnackBar,
              private snackService: SnackMessageService){}

  private cookieLawInit(): void{
    // subscribe to cookieconsent observables to react to main events
    this.popupOpenSubscription = this.ccService.popupOpen$.subscribe(
      () => {
        // you can use this.ccService.getConfig() to do stuff...
      });
 
    this.popupCloseSubscription = this.ccService.popupClose$.subscribe(
      () => {
        // you can use this.ccService.getConfig() to do stuff...
      });
 
    this.initializeSubscription = this.ccService.initialize$.subscribe(
      (event: NgcInitializeEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      });
 
    this.statusChangeSubscription = this.ccService.statusChange$.subscribe(
      (event: NgcStatusChangeEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      });
 
    this.revokeChoiceSubscription = this.ccService.revokeChoice$.subscribe(
      () => {
        // you can use this.ccService.getConfig() to do stuff...
      });
 
    this.noCookieLawSubscription = this.ccService.noCookieLaw$.subscribe(
      (event: NgcNoCookieLawEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      });
  }

  ngOnInit(): void {
    this.cookieLawInit();

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

  ngOnDestroy(): void {
    if (this.popupOpenSubscription !== undefined){
      this.popupOpenSubscription.unsubscribe();
    }
    if (this.popupCloseSubscription !== undefined){
      this.popupCloseSubscription.unsubscribe();
    }
    if (this.initializeSubscription !== undefined){
      this.initializeSubscription.unsubscribe();
    }
    if (this.statusChangeSubscription !== undefined){
      this.statusChangeSubscription.unsubscribe();
    }
    if (this.revokeChoiceSubscription !== undefined){
      this.revokeChoiceSubscription.unsubscribe();
    }
    if (this.noCookieLawSubscription !== undefined){
      this.noCookieLawSubscription.unsubscribe();
    }
    if (this.snackServiceSuscription !== undefined){
      this.snackServiceSuscription.unsubscribe();
    }
    if (this.snackDissmisingSuscription !== undefined){
      this.snackDissmisingSuscription.unsubscribe();
    }
    if (this.snackDismissRequestSuscription !== undefined){
      this.snackDismissRequestSuscription.unsubscribe();
    }
  }

}
