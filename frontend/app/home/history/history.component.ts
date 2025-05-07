import { Component, OnInit, PLATFORM_ID, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
  historyData: any[] = [];

  constructor(
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    this.loadHistory();
  }

  loadHistory() {
    if (isPlatformBrowser(this.platformId)) {
      const savedHistory = localStorage.getItem('conversionHistory');
      if (savedHistory) {
        this.historyData = JSON.parse(savedHistory);
      }
    }
  }

  handleDownload(index: number) {
    if (isPlatformBrowser(this.platformId)) {
      const item = this.historyData[index];
      const blob = new Blob([JSON.stringify(item.content, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = item.fileName.replace(/\.[^/.]+$/, '') + '.json';
      a.click();
    }
  }

  goBack() {
    this.router.navigate(['/']);
  }
}