import { Injectable } from '@angular/core';
import { Observable, of, Subject, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Post} from '../blog/models/post';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseUrl = 'http://localhost:5000/';
  private postSource = new Subject<Post>();

  post$ = this.postSource.asObservable();
  
  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  getPostsInBoard(boardId: number, page: number): Observable<Post[]> {
    let url;

    if (page) {
      url = this.baseUrl + `boards/${boardId}/posts?page=${page}`;
    } else {
      url = this.baseUrl + `boards/${boardId}/posts`;
    }
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>(`getPostsInBoard`, []))
      )
  }

  getPost(idPost: Number): Observable<Post> {
    const url = this.baseUrl + `posts/${idPost}`;
    // let headers: HttpHeaders = new HttpHeaders();
    // let token = this.getToken();
    // if (token) {
    //   headers = headers.set('Authorization', `Bearer ${token}`)
    // }
    return this.http.get<Post>(url)
    .pipe(
      catchError(this.handleError<Post>(`getPost`))
    )
  }

  createPost(body: any, boardId: Number) {
    const url = this.baseUrl + `posts?idBoard=${boardId}`;
    let token = this.getToken();
    return this.http.post(url, body,  
      { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError<Post>(`createPost`))
    )
  }

  updatePost(body: any, postId: Number) {
    const url = this.baseUrl + `posts/${postId}`;
    let token = this.getToken();
    return this.http.patch(url, body, 
      { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError<Post>(`patchPost`))
    )
  }

  deletePost(id: number) {
    const url = this.baseUrl + `posts/${id}`;
    let token = this.getToken();
    return this.http.delete(url, { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError<Post>(`deletePost`))
    )
  }

  likePost(id: number) {
    const url = this.baseUrl + `posts/${id}/like`;
    let token = this.getToken();
    return this.http.patch(url, '', { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError(`likePost`))
    )
  }

  unlikePost(id: number) {
    const url = this.baseUrl + `posts/${id}/unlike`;
    let token = this.getToken();
    return this.http.patch(url, '', { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError(`unlikePost`))
    )
  }

  getPostsRank(): Observable<Post[]> {
    const url = this.baseUrl + `posts/rank`;
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>('getPostsRank'))
    )
  }
  
  private getToken() {
    let token = localStorage.getItem('access_token');
    if (token) {
      return token;
    } else {
      return void 0;
    }
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      let errorMsg = '';
      if (error.error instanceof ErrorEvent) {
        errorMsg = `Error: ${error.error.message}`; 
      } else {
        errorMsg = `Error Code: ${error.status}\nMessage: ${error.message}`
      }
      if(error.status === 401) {
        this.router.navigate(['/member/login'])
      }

      console.error(error);

      window.alert(errorMsg);

      return throwError(errorMsg)

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }), 
  withCredentials: true,
};