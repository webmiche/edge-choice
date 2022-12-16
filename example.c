static void B() { }
static void A() { B(); }

int main() {
  A();
}
