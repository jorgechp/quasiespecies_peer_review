import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ErrorService {
  private errorData$ = new Subject<object>();

  notifyError(data: {}): void {
      this.errorData$.next(data);
  }

  get errorDataObservable(): Observable<object>{
    return this.errorData$.asObservable();
  }

  constructor() { }
}
