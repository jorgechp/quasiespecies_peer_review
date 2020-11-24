import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private registerUserUrl = 'http://0.0.0.0:7000/user/';
  private loginUserUrl = 'http://0.0.0.0:7000/user/login';
  private logoutUserUrl = 'http://0.0.0.0:7000/user/login';


  constructor(private httpClient: HttpClient) { }

  registerUser(userNick: string, userMail: string, userPassword: string): Observable<object>{

    const newUser = {nick: userNick, mail: userMail, password: userPassword};
    return this.httpClient.post(this.registerUserUrl, JSON.stringify(newUser));
  }
}
