static void B() { }
static void G() { B(); }
static void A() { B(); G(); }

int main() {
  A();
}
