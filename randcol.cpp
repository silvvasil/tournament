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
  int color;
  do {
    color = rand() % 6 + 1;
  } while (color == field[0][0] - '0' || color == field[N - 1][M - 1] - '0');
  cout << color << endl;
}

int get_hash() {
  int sumh = 0;
  for (int i = 0; i < N; ++i) {
    sumh += hash<string_view>{}(field[i]);
  }
  return sumh;
}


int main(){
  scan();
  srand(get_hash());
  recolor();
}