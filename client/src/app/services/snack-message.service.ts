import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SnackMessageService {
  private snackMessage$ = new Subject<string>();

  notifyNewSnackMessage(snackMessage: string): void{ this.snackMessage$.next(snackMessage); }

  subscribeSnackMessage(): Observable<string>{ return this.snackMessage$.asObservable(); }

  constructor() { }
}
