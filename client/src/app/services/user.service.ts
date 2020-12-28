import { CONFIG } from '@src/app/config';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { NewUserInterface } from '@src/app/models/new-user-interface.model';
import { tap } from 'rxjs/operators';
import { AbstractControl } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private registerUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/';
  private loginUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/login';
  private logoutUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/logout';
  private changePasswordUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/password';
  private recoveryUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/login/recovery';
  private recoveryUserSecondStageUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/login/recovery/token';

  private isLoggedIn$ = new BehaviorSubject<boolean>(false);
  private isLoggedInObservable = this.isLoggedIn$.asObservable();

  constructor(private httpClient: HttpClient) { }

  getIsLoggedInObservable(): Observable<boolean>{
    return this.isLoggedInObservable;
  }

  checkLogin(): Observable<boolean>{
    return this.httpClient.get<boolean>(this.loginUserUrl, { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(response); })
    );
  }

  registerUser(userNick: string,
               userMail: string,
               userPassword: string,
               isEditor: boolean,
               isReviewer: boolean): Observable<NewUserInterface>{
    const newUser = {nick: userNick,
                    mail: userMail,
                    password: userPassword,
                    editor: isEditor,
                    reviewer: isReviewer};
    return this.httpClient.post<NewUserInterface>(this.registerUserUrl, JSON.stringify(newUser));
  }

  loginUser(userNick: string, userPassword: string): Observable<boolean>{
    const currentUser = {nick: userNick, password: userPassword};
    return this.httpClient.post<boolean>(this.loginUserUrl, JSON.stringify(currentUser), { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(response); } )
    );
  }

  userRecoveryPassword(userNick: string, userMail: string): Observable<boolean>{
    const userData = {nick: userNick, mail: userMail};
    return this.httpClient.post<boolean>(this.recoveryUserUrl, JSON.stringify(userData), { withCredentials: true });
  }

  userChangePassword(currentPassword: string, password1: string): Observable<boolean> {
    const userData = {current_password: currentPassword, new_password: password1};
    return this.httpClient.post<boolean>(this.changePasswordUserUrl, JSON.stringify(userData), { withCredentials: true });
  }

  userRecoveryChangePassword(recoveryToken: string, newPassword: string): Observable<boolean>{
    const userData = {token: recoveryToken, password: newPassword};
    return this.httpClient.post<boolean>(this.recoveryUserSecondStageUrl, JSON.stringify(userData), { withCredentials: true });
  }

  logout(): Observable<boolean>{
    return this.httpClient.post<boolean>(this.logoutUserUrl, JSON.stringify(''), { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(!response); } )
    );
  }
}
