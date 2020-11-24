import { Injectable } from '@angular/core';
import {
    HttpInterceptor,
    HttpRequest,
    HttpResponse,
    HttpHandler,
    HttpEvent,
    HttpErrorResponse
} from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ErrorService } from '@src/app/services/error.service';

@Injectable()
export class InterceptorHttp implements HttpInterceptor {
constructor(public errorService: ErrorService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
        map((event: HttpEvent<any>) => {
            return event;
        }),
        catchError((error: HttpErrorResponse) => {
            let data = {};
            data = {
                reason: error && error.error && error.error.reason ? error.error.reason : '',
                status: error.status,
                error: error.error.message ? error.error.message : ''
            };
            this.errorService.notifyError(data);
            return throwError(error);
        }));
  }
}
