import { Component, OnInit, OnDestroy  } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{
  title = 'quasispecies-peer-review';
  snackServiceSuscription: Subscription | undefined;

  constructor(private snackBar: MatSnackBar,
              private snackService: SnackMessageService){}
  ngOnInit(): void {
    this.snackServiceSuscription = this.snackService.subscribeSnackMessage().subscribe(
      (message: string) => {this.snackBar.open(message, 'Close'); }
    );
  }

  ngOnDestroy(): void {
    if (this.snackServiceSuscription !== undefined){
      this.snackServiceSuscription.unsubscribe();
    }
  }

}
