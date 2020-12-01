import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { SnackBarConfiguration } from '@src/app/models/snackbar-config-interface';

@Injectable({
  providedIn: 'root'
})
export class SnackMessageService {
  private snackMessage$ = new Subject<SnackBarConfiguration>();
  private snackDissmising$ = new Subject<void>();
  private snackDismissRequest$ = new Subject<void>();

  notifyNewSnackMessage(snackMessage: string, snackTime = -1): void{
    const snackConfiguration: SnackBarConfiguration = {message: snackMessage, time: snackTime};
    this.snackMessage$.next(snackConfiguration);
  }

  notifyDissmising(): void{ this.snackDissmising$.next(); }

  notifyDismiss(): void{ this.snackDismissRequest$.next();}

  subscribeSnackMessage(): Observable<SnackBarConfiguration>{ return this.snackMessage$.asObservable(); }

  subscribeDissmising(): Observable<void>{ return this.snackDissmising$.asObservable(); }

  subscribeDismissRequest(): Observable<void>{ return this.snackDismissRequest$.asObservable(); }

  constructor() { }
}
