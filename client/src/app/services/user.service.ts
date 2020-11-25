import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { NewUserInterface } from '@src/app/models/new-user-interface.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private registerUserUrl = 'http://localhost:7000/user';
  private loginUserUrl = 'http://localhost:7000/user/login';
  private logoutUserUrl = 'http://localhost:7000/user/login';


  constructor(private httpClient: HttpClient) { }

  checkLogin(): Observable<boolean>{
    return this.httpClient.get<boolean>(this.loginUserUrl, { withCredentials: true });
  }

  registerUser(userNick: string, userMail: string, userPassword: string): Observable<NewUserInterface>{
    const newUser = {nick: userNick, mail: userMail, password: userPassword};
    return this.httpClient.post<NewUserInterface>(this.registerUserUrl, JSON.stringify(newUser));
  }

  loginUser(userNick: string, userPassword: string): Observable<boolean>{
    const currentUser = {nick: userNick, password: userPassword};
    return this.httpClient.post<boolean>(this.loginUserUrl, JSON.stringify(currentUser), { withCredentials: true });
  }

  logout(): Observable<boolean>{
    return this.httpClient.delete<boolean>(this.logoutUserUrl);
  }
}
