import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { NewUserInterface } from '@src/app/models/new-user-interface.model';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private registerUserUrl = 'http://localhost:7000/user/';
  private loginUserUrl = 'http://localhost:7000/user/login';
  private logoutUserUrl = 'http://localhost:7000/user/logout';

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

  registerUser(userNick: string, userMail: string, userPassword: string): Observable<NewUserInterface>{
    const newUser = {nick: userNick, mail: userMail, password: userPassword};
    return this.httpClient.post<NewUserInterface>(this.registerUserUrl, JSON.stringify(newUser));
  }

  loginUser(userNick: string, userPassword: string): Observable<boolean>{
    const currentUser = {nick: userNick, password: userPassword};
    return this.httpClient.post<boolean>(this.loginUserUrl, JSON.stringify(currentUser), { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(response); } )
    );
  }

  logout(): Observable<boolean>{
    return this.httpClient.post<boolean>(this.logoutUserUrl, JSON.stringify(''), { withCredentials: true }).pipe(
      tap((response: boolean) => {this.isLoggedIn$.next(!response); } )
    );
  }
}
