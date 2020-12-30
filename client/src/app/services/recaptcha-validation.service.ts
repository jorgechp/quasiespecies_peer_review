import { Observable } from 'rxjs';
import { Injectable, OnDestroy } from '@angular/core';
import {HttpClient } from '@angular/common/http'
import { CONFIG } from '@src/app/config';

@Injectable({
  providedIn: 'root'
})
export class RecaptchaValidationService {

  constructor(private http: HttpClient) { }


  sendToken(token: string): Observable<any>{
    return this.http.post<any>(CONFIG.TOKEN_VALIDATOR_HOST + '/token_validate' + ':' + CONFIG.TOKEN_VALIDATOR_PORT, {recaptcha: token});
  }
}
