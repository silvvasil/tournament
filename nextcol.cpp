#include <bits/stdc++.h>

using namespace std;

const int N = 41;
const int M = 45;

string field[N];

bool scan(){
  for (int i = 0; i < N; ++i) {
    if (!(cin >> field[i])) {
      return false;
    }
  }
  return true;
}

void recolor() {
  int color = field[0][0] - '0';
  for (int it = 0; it < 6; ++it) {
    int ncolor = (color + it);
    if (ncolor > 6) {
      ncolor -= 6;
    }
    if (ncolor == field[0][0] - '0' || ncolor == field[N - 1][M - 1] - '0') {
      continue;
    }
    cout << ncolor << endl;
    break;
  }
}

int main(){
  scan();
  recolor();
}