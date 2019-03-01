import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Comment } from '../blog/models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private baseUrl = 'http://0.0.0.0:5000/';

  constructor(
    private http: HttpClient,
  ) { }

  getCommentsInPost(idPost: number): Observable<Comment[]> {
    const url = this.baseUrl + `posts/${idPost}/comments`;
    return this.http.get<Comment[]>(url)
    .pipe(
      catchError(this.handleError<Comment[]>(`getPostsInBoard`))
      )
  }

  createComment(commentForm: any, idPost: number, idComment: number) {
    const url = this.baseUrl + `comments?idPost=${idPost}&idComment:${idComment}`;
    // const url = this.baseUrl + `?idPost=${idPost}&idComment:${idComment}`;
    return this.http.post(url, commentForm, httpOptions)
    .pipe(
      catchError(this.handleError<Comment>(`createComment`))
    )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error('error'); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  withCredentials: true
};