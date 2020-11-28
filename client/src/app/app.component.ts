import { Component, OnInit, OnDestroy  } from '@angular/core';
import {MatSnackBar, MatSnackBarRef, TextOnlySnackBar} from '@angular/material/snack-bar';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { Subscription } from 'rxjs';
import { SnackBarConfiguration } from '@src/app/models/snackbar-config-interface';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{
  title = 'quasispecies-peer-review';
  snackServiceSuscription: Subscription | undefined;
  snackDissmisingSuscription: Subscription | undefined;

  constructor(private snackBar: MatSnackBar,
              private snackService: SnackMessageService){}
  ngOnInit(): void {
    this.snackServiceSuscription = this.snackService.subscribeSnackMessage().subscribe(
        (message: SnackBarConfiguration) => {
          let snackBarRef: MatSnackBarRef<TextOnlySnackBar>;
          if (message.time < 0 ){
            snackBarRef = this.snackBar.open(message.message, 'Close');
          }else{
            snackBarRef = this.snackBar.open(message.message, 'Close', {duration: message.time});
          }
          snackBarRef.afterDismissed().subscribe(
            () => {
              this.snackService.notifyDissmising();
            }
          );
      }
    );
  }

  ngOnDestroy(): void {
    if (this.snackServiceSuscription !== undefined){
      this.snackServiceSuscription.unsubscribe();
    }
    if (this.snackDissmisingSuscription !== undefined){
      this.snackDissmisingSuscription.unsubscribe();
    }
  }

}
