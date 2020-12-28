import { CONFIG } from '@src/app/config';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { NewUserInterface } from '@src/app/models/new-user-interface.model';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private userUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/';
  private userDeleteUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/delete';
  private loginUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/login';
  private logoutUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/logout';
  private changePasswordUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/password';
  private mailUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/mail';
  private roleUserUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/user/role';
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
    return this.httpClient.post<NewUserInterface>(this.userUrl, JSON.stringify(newUser));
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

  userMail(): Observable<string>{
    return this.httpClient.get<string>(this.mailUserUrl, { withCredentials: true });
  }

  userChangeMail(currentPassword: string, mail: string): Observable<boolean> {
    const userData = {current_password: currentPassword, new_mail: mail};
    return this.httpClient.post<boolean>(this.mailUserUrl, JSON.stringify(userData), { withCredentials: true });
  }

  userRecoveryChangePassword(recoveryToken: string, newPassword: string): Observable<boolean>{
    const userData = {token: recoveryToken, password: newPassword};
    return this.httpClient.post<boolean>(this.recoveryUserSecondStageUrl, JSON.stringify(userData), { withCredentials: true });
  }

  getUserRole(): Observable<Array<string>> {
    return this.httpClient.get<Array<string>>(this.roleUserUrl, { withCredentials: true });
  }

  userChangeRole(currentPasswordValue: string, imEditor: boolean, imReviewer: boolean): Observable<boolean> {
    const userData = {current_password: currentPasswordValue, editor: imEditor, reviewer: imReviewer};
    return this.httpClient.post<boolean>(this.roleUserUrl, JSON.stringify(userData), { withCredentials: true });
  }

  deleteAccount(currentPasswordValue: string): Observable<boolean>  {
    const userData = {current_password: currentPasswordValue};
    return this.httpClient.post<boolean>(this.userDeleteUrl, JSON.stringify(userData), { withCredentials: true });
  }

  logout(): Observable<boolean>{
    return this.httpClient.post<boolean>(this.logoutUserUrl, JSON.stringify(''), { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(!response); } )
    );
  }
}
