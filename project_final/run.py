from multiprocessing import Process, Pipe
import perception
import interaction
if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    signal1,signal2 = Pipe()
    p1 = Process(target=perception.main, args=(child_conn,signal1))
    p1.start()

   

    p2 = Process(target=interaction.demo_personas, args=(parent_conn,signal2))
    p2.start()

    p1.join()
    p2.join()
    


    parent_conn.close()
    child_conn.close()
    