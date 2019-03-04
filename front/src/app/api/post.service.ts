import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Post, PostForm } from '../blog/models/post';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseUrl = 'http://localhost:5000/';
  private postSource = new Subject<Post>();

  post$ = this.postSource.asObservable();
  
  constructor(
    private http: HttpClient
  ) { }

  getPostsInBoard(idBoard: number): Observable<Post[]> {
    const url = this.baseUrl + `boards/${idBoard}/posts`;
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>(`getPostsInBoard`, []))
      )
  }

  getPost(idPost: number): Observable<Post> {
    const url = this.baseUrl + `posts/${idPost}`;
    return this.http.get<Post>(url)
    .pipe(
      catchError(this.handleError<Post>(`getPost`))
    )
  }

  createPost(body: any, idBoard: any) {
    const url = this.baseUrl + `posts?idBoard=${idBoard}`;
    let token = this.getToken();
    return this.http.post(url, body,  
      { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError<Post>(`createPost`))
    )
  }

  updatePost(id: number) {
    const url = this.baseUrl + `posts/${id}`;
    let token = this.getToken();
    return this.http.patch(url, { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
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

  private getToken() {
    return localStorage.getItem('access_token')
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }), 
  withCredentials: true,
};