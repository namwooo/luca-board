import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TokenService } from '../shared/services/token.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

    constructor(
        private tokenService: TokenService,
    ) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        debugger;
        request = request.clone({
            setHeaders: {
                Authorization: `Bearer ${this.tokenService.getToken()}`
            }
        });
        
        return next.handle(request);
    }
}
