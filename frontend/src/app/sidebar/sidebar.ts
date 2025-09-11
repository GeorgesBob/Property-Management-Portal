import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true, // ✅ confirm it's standalone
  imports: [RouterLink, RouterLinkActive], // ✅ add RouterLinkActive here
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss']  // ⚡ should be plural: styleUrls
})
export class SidebarComponent {}
