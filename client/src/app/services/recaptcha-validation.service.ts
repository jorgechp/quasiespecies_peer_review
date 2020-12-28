import { Observable } from 'rxjs';
import { Injectable, OnDestroy } from '@angular/core';
import {HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class RecaptchaValidationService {

  constructor(private http: HttpClient) { }


  sendToken(token: string): Observable<any>{
    return this.http.post<any>('/token_validate', {recaptcha: token});
  }
}
